from datetime import datetime
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from ..models import *


def is_instructor_check(user):
    return user.is_instructor


@method_decorator(user_passes_test(is_instructor_check), name='dispatch')
class AssignmentCreate(LoginRequiredMixin, CreateView):
    model = Assignment
    template_name = './assignment_create.html'
    fields = ['name', 'description', 'start_date', 'end_date', 'course', 'environment_definition']

    def form_valid(self, form):
        return super(AssignmentCreate, self).form_valid(form)


class AssignmentDetail(LoginRequiredMixin, DetailView):
    template_name = './assignment_detail.html'

    def get_queryset(self):
        return Assignment.objects.filter(course__in=self.request.user.instructs.all()) | Assignment.objects.filter(
            course__in=self.request.user.courses.all(), start_date__gte=datetime.now(), end_date__lte=datetime.now())


class AssignmentList(LoginRequiredMixin, ListView):
    template_name = './assignment_list.html'

    def get_queryset(self):
        return Assignment.objects.filter(course__in=self.request.user.instructs.all()) | Assignment.objects.filter(
            course__in=self.request.user.courses.all(), start_date__gte=datetime.now(), end_date__lte=datetime.now())


@method_decorator(user_passes_test(is_instructor_check), name='dispatch')
class AssignmentUpdate(LoginRequiredMixin, UpdateView):
    template_name = './assignment_update.html'
    fields = ['name', 'description', 'start_date', 'end_date', 'course', 'environment_definition']

    def get_queryset(self):
        return Assignment.objects.filter(course__in=self.request.user.instructs.all())


@method_decorator(user_passes_test(is_instructor_check), name='dispatch')
class AssignmentDelete(LoginRequiredMixin, DeleteView):
    template_name = './assignment_delete.html'
    success_url = reverse_lazy('assignments')

    def get_queryset(self):
        return Assignment.objects.filter(course__in=self.request.user.instructs.all())
