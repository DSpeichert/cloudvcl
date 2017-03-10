from django.views.generic import CreateView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import *


class EnvironmentDefinitionCreate(LoginRequiredMixin, CreateView):
    model = EnvironmentDefinition
    template_name = './environment_definition_create.html'
    fields = ['name']

    def form_valid(self, form):
        form.instance.instructor_id = self.request.user.id
        return super(EnvironmentDefinitionCreate, self).form_valid(form)


class EnvironmentDefinitionDetail(LoginRequiredMixin, DetailView):
    model = EnvironmentDefinition
    template_name = './environment_definition_detail.html'


class EnvironmentDefinitionList(LoginRequiredMixin, ListView):
    model = EnvironmentDefinition
    template_name = './environment_definition_list.html'
