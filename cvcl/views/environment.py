from django.http import HttpResponseNotFound
from django.views.generic import DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.db.models import Q
from ..models import *


class EnvironmentDetail(LoginRequiredMixin, DetailView):
    model = Environment
    template_name = './environment_detail.html'

    def get_queryset(self):
        queryset = super(EnvironmentDetail, self).get_queryset()
        return queryset.filter(
            Q(user=self.request.user) | Q(assignment__course__instructor=self.request.user)).prefetch_related()

    def get_context_data(self, **kwargs):
        context = super(EnvironmentDetail, self).get_context_data(**kwargs)
        if self.kwargs.get('uuid', None) is not None:
            try:
                context['vm'] = self.object.vms.get(uuid=self.kwargs.get('uuid', None))
            except Vm.DoesNotExist:
                return HttpResponseNotFound('<h1>VM not found</h1>')
        else:
            context['vm'] = self.object.vms.first()

        try:
            context['vnc'] = context['vm'].get_vnc()
        except:
            pass

        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        if self.kwargs.get('uuid', None) is None:
            first_vm = self.object.vms.first()
            if first_vm is not None:
                return redirect(first_vm)
        return self.render_to_response(context)


class EnvironmentDelete(LoginRequiredMixin, DeleteView):
    model = Environment
    template_name = './environment_delete.html'

    def get_queryset(self):
        queryset = super(EnvironmentDelete, self).get_queryset()
        return queryset.filter(
            Q(user=self.request.user) | Q(assignment__course__instructor=self.request.user))

    def get_success_url(self):
        return reverse_lazy('assignments.detail', kwargs={'pk': self.object.assignment.id})
