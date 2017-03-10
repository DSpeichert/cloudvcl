from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from ..models import *


class AssignmentList(LoginRequiredMixin, ListView):
    template_name = './assignment_list.html'

    def get_queryset(self):
        return Assignment.objects.filter()


@method_decorator(require_http_methods("GET"), name='dispatch')
class AssignmentDetail(DetailView):
    model = Assignment
    template_name = './assignment_detail.html'
