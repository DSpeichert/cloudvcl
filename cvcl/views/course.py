from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import user_passes_test
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.db.models import Q
from ..models import *
from ..forms import CourseUploadCsvForm


def is_instructor_check(user):
    return user.is_instructor


@method_decorator(user_passes_test(is_instructor_check), name='dispatch')
class CourseCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Course
    template_name = './course_create.html'
    fields = ['name', 'students']
    success_message = "%(name)s was created successfully"

    def form_valid(self, form):
        form.instance.instructor = self.request.user
        return super(CourseCreate, self).form_valid(form)


class CourseDetail(LoginRequiredMixin, DetailView):
    template_name = './course_detail.html'

    def get_queryset(self):
        return Course.objects.filter(
            Q(instructor=self.request.user) | Q(students__exact=self.request.user)).distinct().prefetch_related()


class CourseList(LoginRequiredMixin, ListView):
    template_name = './course_list.html'

    def get_queryset(self):
        return Course.objects.filter(Q(instructor=self.request.user) | Q(students__exact=self.request.user)).distinct()


@method_decorator(user_passes_test(is_instructor_check), name='dispatch')
class CourseUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = './course_update.html'
    fields = ['name', 'students']
    success_message = "%(name)s was updated successfully"

    def get_queryset(self):
        return Course.objects.filter(instructor=self.request.user)


@method_decorator(user_passes_test(is_instructor_check), name='dispatch')
class CourseDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    template_name = './course_delete.html'
    success_url = reverse_lazy('courses')
    success_message = "%(name)s was deleted successfully"

    def get_queryset(self):
        return Course.objects.filter(instructor=self.request.user)


@method_decorator(user_passes_test(is_instructor_check), name='dispatch')
class CourseRemoveStudent(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Course
    template_name = 'course_remove_student.html'

    def get_context_data(self, **kwargs):
        context = super(CourseRemoveStudent, self).get_context_data(**kwargs)
        try:
            context['student'] = User.objects.get(pk=self.kwargs['student_pk'])
            if context['student'] not in context['course'].students.all():
                raise Http404('No student matches the given query.')
        except User.DoesNotExist:
            raise Http404('No student matches the given query.')
        return context

    def delete(self, request, *args, **kwargs):
        course = self.get_object()
        student = User.objects.get(pk=self.kwargs['student_pk'])
        if student not in course.students.all():
            messages.error(request, 'This student is not in this course!')
            return HttpResponseRedirect(reverse_lazy('courses.detail', kwargs={'pk': course.pk}))

        for assignment in course.assignments.all():
            assignment.environments.filter(user=student).delete()

        course.students.remove(student)
        return HttpResponseRedirect(reverse_lazy('courses.detail', kwargs={'pk': course.pk}))

    def get_queryset(self):
        return Course.objects.filter(instructor=self.request.user)

    def get_success_url(self):
        return reverse_lazy('courses.detail', kwargs={'pk': self.kwargs['pk']})


@method_decorator(user_passes_test(is_instructor_check), name='dispatch')
class CourseAddStudents(LoginRequiredMixin, SuccessMessageMixin, FormView):
    template_name = 'course_upload_csv_form.html'
    form_class = CourseUploadCsvForm

    def get_context_data(self, **kwargs):
        context = super(CourseAddStudents, self).get_context_data(**kwargs)
        context['course'] = get_object_or_404(Course, pk=self.kwargs['pk'])
        return context

    # Checks if the user is the instructor for this course
    def get(self, request, *args, **kwargs):
        course = get_object_or_404(Course, pk=self.kwargs['pk'])
        if not course.instructor == self.request.user:
            return redirect("courses")
        return super(CourseAddStudents, self).get(request, *args, **kwargs)

    # Checks if the user is the instructor for this course
    def post(self, request, *args, **kwargs):
        course = get_object_or_404(Course, pk=self.kwargs['pk'])
        if not course.instructor == self.request.user:
            return redirect("courses")
        return super(CourseAddStudents, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        form.process_data(self.kwargs['pk'])
        return super(CourseAddStudents, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('courses.detail', kwargs={'pk': self.kwargs['pk']})
