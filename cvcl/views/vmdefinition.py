from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from ..models import *


def is_instructor_check(user):
    return user.is_instructor


@method_decorator(user_passes_test(is_instructor_check), name='dispatch')
class VmDefinitionCreate(LoginRequiredMixin, CreateView):
    model = VmDefinition
    template_name = './vm_definition_create.html'
    fields = ['name', 'image', 'flavor', 'user_script']

    def form_valid(self, form):
        form.instance.environment_id = self.kwargs['pk']
        # TODO check if image is allowed for instructor
        return super(VmDefinitionCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('envdefs.detail', kwargs=self.kwargs)


@method_decorator(user_passes_test(is_instructor_check), name='dispatch')
class VmDefinitionDetail(LoginRequiredMixin, DetailView):
    template_name = './vm_definition_detail.html'
    context_object_name = 'vm_definition'

    def get_queryset(self):
        return VmDefinition.objects.filter(environment__in=self.request.user.environment_definitions.all())


@method_decorator(user_passes_test(is_instructor_check), name='dispatch')
class VmDefinitionUpdate(LoginRequiredMixin, UpdateView):
    template_name = './vm_definition_update.html'
    fields = ['name', 'image', 'flavor', 'user_script']

    def get_queryset(self):
        return VmDefinition.objects.filter(environment__in=self.request.user.environment_definitions.all())


@method_decorator(user_passes_test(is_instructor_check), name='dispatch')
class VmDefinitionDelete(LoginRequiredMixin, DeleteView):
    template_name = './vm_definition_delete.html'

    def get_success_url(self):
        return reverse('envdefs.detail', kwargs=self.kwargs)

    def get_queryset(self):
        return VmDefinition.objects.filter(environment__in=self.request.user.environment_definitions.all())
