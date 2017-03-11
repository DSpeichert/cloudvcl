from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from ..models import *
from ..forms import VmDefinitionForm


def is_instructor_check(user):
    return user.is_instructor


@method_decorator(user_passes_test(is_instructor_check), name='dispatch')
class VmDefinitionCreate(LoginRequiredMixin, CreateView):
    template_name = './vm_definition_create.html'
    form_class = VmDefinitionForm

    def get_form_kwargs(self):
        kwargs = super(VmDefinitionCreate, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.environment_id = self.kwargs['pk']
        return super(VmDefinitionCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('envdefs.detail', kwargs=self.kwargs)


@method_decorator(user_passes_test(is_instructor_check), name='dispatch')
class VmDefinitionUpdate(LoginRequiredMixin, UpdateView):
    template_name = './vm_definition_update.html'
    form_class = VmDefinitionForm

    def get_form_kwargs(self):
        kwargs = super(VmDefinitionUpdate, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_queryset(self):
        return VmDefinition.objects.filter(environment__in=self.request.user.environment_definitions.all())


@method_decorator(user_passes_test(is_instructor_check), name='dispatch')
class VmDefinitionDelete(LoginRequiredMixin, DeleteView):
    template_name = './vm_definition_delete.html'

    def get_success_url(self):
        return reverse('envdefs.detail', kwargs=self.kwargs)

    def get_queryset(self):
        return VmDefinition.objects.filter(environment__in=self.request.user.environment_definitions.all())
