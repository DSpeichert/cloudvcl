from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import *


class EnvironmentDetail(LoginRequiredMixin, DetailView):
    model = Environment
    template_name = './environment_detail.html'

    def get_queryset(self):
        queryset = super(EnvironmentDetail, self).get_queryset()
        return queryset.filter(user=self.request.user)
