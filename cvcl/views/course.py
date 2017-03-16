from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import user_passes_test
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.db.models import Q
from ..models import *


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
