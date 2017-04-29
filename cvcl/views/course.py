from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import user_passes_test
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseRedirect
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
class CourseDeleteStudents(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Course
    template_name = 'course_detail.html'

    def get(self, request, *args, **kwargs):
        course = get_object_or_404(Course, pk=self.kwargs['pk'])
        if not course.instructor == self.request.user:
            return redirect("courses")
        return super(CourseDeleteStudents, self).get(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        user = User.objects.get(pk=self.kwargs['user_pk'])
        self.object.students.remove(user)
        return HttpResponseRedirect(reverse_lazy('courses.detail', kwargs={'pk': self.object.pk}))

    def get_queryset(self):
        return Course.objects.filter(instructor=self.request.user)


@method_decorator(user_passes_test(is_instructor_check), name='dispatch')
class CourseAddStudents(LoginRequiredMixin, SuccessMessageMixin, FormView):
    template_name = 'user_upload.html'
    form_class = CourseUploadCsvForm

    # Checks if the user is the instructor for this course
    def get(self, request, *args, **kwargs):
        course = get_object_or_404(Course, pk=self.kwargs['pk'])
        if not course.instructor == self.request.user:
            return redirect("courses")
        return super(CourseAddStudents, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        course_id = self.kwargs['pk']
        course = get_object_or_404(Course, pk=course_id)
        if course.instructor != self.request.user:
            return redirect("courses")
        form.process_data(course_id)
        return super(CourseAddStudents, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('courses.detail', kwargs={'pk': self.kwargs['pk']})

    def get_queryset(self):
        return Course.objects.filter(instructor=self.request.user)
