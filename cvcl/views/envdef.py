from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from ..models import *


def is_instructor_check(user):
    return user.is_instructor


@method_decorator(user_passes_test(is_instructor_check), name='dispatch')
class EnvironmentDefinitionCreate(LoginRequiredMixin, CreateView):
    model = EnvironmentDefinition
    template_name = './environment_definition_create.html'
    fields = ['name']

    def form_valid(self, form):
        form.instance.instructor_id = self.request.user.id
        return super(EnvironmentDefinitionCreate, self).form_valid(form)


@method_decorator(user_passes_test(is_instructor_check), name='dispatch')
class EnvironmentDefinitionDetail(LoginRequiredMixin, DetailView):
    template_name = './environment_definition_detail.html'

    def get_queryset(self):
        return EnvironmentDefinition.objects.filter(instructor_id=self.request.user.id)


@method_decorator(user_passes_test(is_instructor_check), name='dispatch')
class EnvironmentDefinitionList(LoginRequiredMixin, ListView):
    template_name = './environment_definition_list.html'

    def get_queryset(self):
        return EnvironmentDefinition.objects.filter(instructor_id=self.request.user.id)


@method_decorator(user_passes_test(is_instructor_check), name='dispatch')
class EnvironmentDefinitionUpdate(LoginRequiredMixin, UpdateView):
    template_name = './environment_definition_update.html'
    fields = ['name']

    def get_queryset(self):
        return EnvironmentDefinition.objects.filter(instructor_id=self.request.user.id)


@method_decorator(user_passes_test(is_instructor_check), name='dispatch')
class EnvironmentDefinitionDelete(LoginRequiredMixin, DeleteView):
    template_name = './environment_definition_delete.html'
    success_url = reverse_lazy('envdefs')

    def get_queryset(self):
        return EnvironmentDefinition.objects.filter(instructor_id=self.request.user.id)
