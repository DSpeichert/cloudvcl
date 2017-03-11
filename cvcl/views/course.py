from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from ..models import *


def is_instructor_check(user):
    return user.is_instructor


@method_decorator(user_passes_test(is_instructor_check), name='dispatch')
class CourseCreate(LoginRequiredMixin, CreateView):
    model = Course
    template_name = './course_create.html'
    fields = ['name', 'students']

    def form_valid(self, form):
        form.instance.instructor = self.request.user
        return super(CourseCreate, self).form_valid(form)


@method_decorator(user_passes_test(is_instructor_check), name='dispatch')
class CourseDetail(LoginRequiredMixin, DetailView):
    template_name = './course_detail.html'

    def get_queryset(self):
        return Course.objects.filter(instructor=self.request.user)


class CourseList(LoginRequiredMixin, ListView):
    template_name = './course_list.html'

    def get_queryset(self):
        return self.request.user.instructs.all() | self.request.user.courses.all()


@method_decorator(user_passes_test(is_instructor_check), name='dispatch')
class CourseUpdate(LoginRequiredMixin, UpdateView):
    template_name = './course_update.html'
    fields = ['name', 'students']

    def get_queryset(self):
        return Course.objects.filter(instructor=self.request.user)


@method_decorator(user_passes_test(is_instructor_check), name='dispatch')
class CourseDelete(LoginRequiredMixin, DeleteView):
    template_name = './course_delete.html'
    success_url = reverse_lazy('courses')

    def get_queryset(self):
        return Course.objects.filter(instructor=self.request.user)
