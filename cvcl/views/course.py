from django.views.generic import ListView
from ..models import *


class CourseList(ListView):
    model = Course
    template_name = './course_list.html'
