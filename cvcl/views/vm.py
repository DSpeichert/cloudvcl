from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import *


class VMDetail(LoginRequiredMixin, DetailView):
    model = Vm
    template_name = './VM_detail.html'

    def get_queryset(self):
        queryset = super(VMDetail, self).get_queryset()
        return queryset.filter(user=self.request.user)

# class Vm(models.Model):
#     uuid = models.CharField(max_length=36)
#     ip_address = models.GenericIPAddressField()
#     environment = models.ForeignKey('Environment', on_delete=models.CASCADE)
#     vm_definition = models.ForeignKey('VmDefinition')
#
#     def __str__(self):
#         return self.uuid
