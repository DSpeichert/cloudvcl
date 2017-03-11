from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from ..models import *


def is_instructor_check(user):
    return user.is_instructor


@method_decorator(user_passes_test(is_instructor_check), name='dispatch')
class VmDefCreate(LoginRequiredMixin, CreateView):
    model = VmDefinition
    # template_name =
    fields = ['name', 'environment', 'image', 'flavor', 'user_script']

    def form_valid(self, form):
        form.instance.instructor_id = self.request.user.id
        return super(VmDefCreate, self).form_valid(form)


@method_decorator(user_passes_test(is_instructor_check), name='dispatch')
class VmDefDetail(LoginRequiredMixin, DetailView):
    # template_name =
    def get_queryset(self):
        return VmDefinition.objects.filter(instructor_id=self.request.user.id)


@method_decorator(user_passes_test(is_instructor_check), name='dispatch')
class VmDefList(LoginRequiredMixin, ListView):
    # template_name
    #   fields = ['name','environment','image','flavor','user_script']
    def get_queryset(self):
        # need to change this
        return VmDefinition.objects.filter(instructor_id=self.request.user.id)


@method_decorator(user_passes_test(is_instructor_check), name='dispatch')
class VmDefUpdate(LoginRequiredMixin, UpdateView):
    # template_name =
    fields = ['name', 'environment', 'image', 'flavor', 'user_script']

    def get_queryset(self):
        return VmDefinition.objects.filter(instructor_id=self.request.user.id)


@method_decorator(user_passes_test(is_instructor_check), name='dispatch')
class VMDefDelete(LoginRequiredMixin, DeleteView):
    # template_name =
    success_url = reverse_lazy('vmdefs')

    def get_queryset(self):
        return VmDefinition.objects.filter(instructor_id=self.request.user.id)
