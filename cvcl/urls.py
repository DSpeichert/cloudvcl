from django.conf.urls import url
from . import views
from cvcl.views import *

urlpatterns = [
    url(r'^$', views.index, name='index'),  # welcome page for all
    url(r'^assignments$', AssignmentList.as_view()),  # student, instructor (list)
    # url(r'^environment/:id$', UserQuota.as_view()),  # student (sees environment)
    # url(r'^assignments/:id$', UserQuota.as_view()),  # instructor (edits assignment)
    # url(r'^assignments/create$', ),
    url(r'^courses$', CourseList.as_view()),  # student, instructor
    # url(r'^courses/:id$', UserGroup.as_view()),  # instructor (edits course: add/remove students)
    url(r'^envdefs$', EnvironmentDefinitionList.as_view()),  # instructor
]
