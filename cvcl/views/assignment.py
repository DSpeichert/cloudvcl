from django.views.generic import ListView
from ..models import *


class AssignmentList(ListView):
    model = Assignment
    template_name = './assignment_list.html'
