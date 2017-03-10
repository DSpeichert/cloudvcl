from django.views.generic import ListView
from ..models import *


class EnvironmentDefinitionList(ListView):
    model = EnvironmentDefinition
    template_name = './environment_definition_list.html'
