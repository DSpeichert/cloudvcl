from django.views.generic import DetailView
from ..models import *


class EnvironmentDetail(DetailView):
    model = Environment
    template_name = './environment_detail.html'
