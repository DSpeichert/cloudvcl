from django.views.generic import DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from ..models import *


class EnvironmentDetail(LoginRequiredMixin, DetailView):
    model = Environment
    template_name = './environment_detail.html'

    def get_queryset(self):
        queryset = super(EnvironmentDetail, self).get_queryset()
        return queryset.filter(user=self.request.user)


class EnvironmentDelete(LoginRequiredMixin, DeleteView):
    model = Environment
    template_name = './environment_delete.html'

    def get_queryset(self):
        queryset = super(EnvironmentDelete, self).get_queryset()
        return queryset.filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('assignments.detail', kwargs={'pk': self.object.assignment.id})
