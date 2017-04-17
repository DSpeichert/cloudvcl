from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from cvcl.views import *
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),  # welcome page for all
    url(r'^logout$', views.logout, name='logout'),  # logout page for all
    url(r'^environments/(?P<pk>\d+)(?:/vm/(?P<uuid>[a-z0-9\-]+))?$', EnvironmentDetail.as_view(),
        name='environments.detail'),
    url(r'^environments/(?P<pk>\d+)/delete$', EnvironmentDelete.as_view(), name='environments.delete'),
    url(r'^assignments$', AssignmentList.as_view(), name='assignments'),  # student, instructor (list)
    url(r'^assignments/create$', AssignmentCreate.as_view(), name='assignments.create'),  # instructor
    url(r'^assignments/(?P<pk>\d+)$', AssignmentDetail.as_view(), name='assignments.detail'),  # instructor
    url(r'^assignments/(?P<pk>\d+)/update$', AssignmentUpdate.as_view(), name='assignments.update'),  # instructor
    url(r'^assignments/(?P<pk>\d+)/delete$', AssignmentDelete.as_view(), name='assignments.delete'),  # instructor
    url(r'^assignments/(?P<pk>\d+)/launch', AssignmentLaunch.as_view(), name='assignments.launch'),  # student
    url(r'^courses$', CourseList.as_view(), name='courses'),  # student, instructor
    url(r'^courses/create$', CourseCreate.as_view(), name='courses.create'),  # instructor
    url(r'^courses/(?P<pk>\d+)$', CourseDetail.as_view(), name='courses.detail'),  # instructor
    url(r'^courses/(?P<pk>\d+)/update$', CourseUpdate.as_view(), name='courses.update'),  # instructor
    url(r'^courses/(?P<pk>\d+)/delete$', CourseDelete.as_view(), name='courses.delete'),  # instructor
    url(r'^envdefs$', EnvironmentDefinitionList.as_view(), name='envdefs'),  # instructor
    url(r'^envdefs/create$', EnvironmentDefinitionCreate.as_view(), name='envdefs.create'),  # instructor
    url(r'^envdefs/(?P<pk>\d+)$', EnvironmentDefinitionDetail.as_view(), name='envdefs.detail'),  # instructor
    url(r'^envdefs/(?P<pk>\d+)/update$', EnvironmentDefinitionUpdate.as_view(), name='envdefs.update'),  # instructor
    url(r'^envdefs/(?P<pk>\d+)/delete$', EnvironmentDefinitionDelete.as_view(), name='envdefs.delete'),  # instructor
    url(r'^envdefs/(?P<pk>\d+)/createvmdef$', VmDefinitionCreate.as_view(), name='envdefs.createvmdef'),  # instructor
    url(r'^vmdefinitions/(?P<pk>\d+)/update$', VmDefinitionUpdate.as_view(), name='vmdef.update'),  # instructor
    url(r'^vmdefinitions/(?P<pk>\d+)/delete$', VmDefinitionDelete.as_view(), name='vmdef.delete'),  # instructor
                  url(r'^upload/', addreport, name='csv_upload'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
