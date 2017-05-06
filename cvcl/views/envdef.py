from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import user_passes_test
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from ..models import *


def is_instructor_check(user):
    return user.is_authenticated and user.is_instructor


@method_decorator(user_passes_test(is_instructor_check), name='dispatch')
class EnvironmentDefinitionCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = EnvironmentDefinition
    context_object_name = 'environment_definition'
    template_name = './environment_definition_create.html'
    fields = ['name']
    success_message = "%(name)s was created successfully"

    def form_valid(self, form):
        form.instance.instructor_id = self.request.user.id
        return super(EnvironmentDefinitionCreate, self).form_valid(form)


@method_decorator(user_passes_test(is_instructor_check), name='dispatch')
class EnvironmentDefinitionDetail(LoginRequiredMixin, DetailView):
    template_name = './environment_definition_detail.html'
    context_object_name = 'environment_definition'

    def get_queryset(self):
        return EnvironmentDefinition.objects.filter(instructor_id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super(EnvironmentDefinitionDetail, self).get_context_data(**kwargs)
        context['vm_definitions'] = VmDefinition.objects.filter(environment_id=kwargs['object'].id)
        return context


@method_decorator(user_passes_test(is_instructor_check), name='dispatch')
class EnvironmentDefinitionList(LoginRequiredMixin, ListView):
    template_name = './environment_definition_list.html'

    def get_queryset(self):
        return EnvironmentDefinition.objects.filter(instructor_id=self.request.user.id)


@method_decorator(user_passes_test(is_instructor_check), name='dispatch')
class EnvironmentDefinitionUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = './environment_definition_update.html'
    context_object_name = 'environment_definition'
    fields = ['name']
    success_message = "%(name)s was updated successfully"

    def get_queryset(self):
        return EnvironmentDefinition.objects.filter(instructor_id=self.request.user.id)


@method_decorator(user_passes_test(is_instructor_check), name='dispatch')
class EnvironmentDefinitionDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    template_name = './environment_definition_delete.html'
    context_object_name = 'environment_definition'
    success_url = reverse_lazy('envdefs')
    success_message = "%(name)s was deleted successfully"

    def get_queryset(self):
        return EnvironmentDefinition.objects.filter(instructor_id=self.request.user.id)
