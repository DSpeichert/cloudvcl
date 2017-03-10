from django.conf.urls import url

from cvcl.views import *
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),  # welcome page for all
    url(r'^logout$', views.logout, name='logout'),  # logout page for all
    url(r'^assignments', AssignmentList.as_view(), name='assignments'),  # student, instructor (list)
    url(r'^environments/(?P<id>\d+)$', EnvironmentDetail.as_view()),  # student (sees environment)
    url(r'^assignments/(?P<id>\d+)$$', AssignmentDetail.as_view()),  # instructor (edits assignment)
    # url(r'^assignments/create$', ),
    url(r'^courses$', CourseList.as_view()),  # student, instructor
    # url(r'^courses/:id$', UserGroup.as_view()),  # instructor (edits course: add/remove students)
    url(r'^envdefs$', EnvironmentDefinitionList.as_view()),  # instructor
]
