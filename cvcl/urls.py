from django.conf.urls import url
from . import views
from cvcl.views import *

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^users/$', UserList.as_view()),
    url(r'^usergroups/$', UserGroup.as_view()),
    url(r'usergroups/add/$', UserGroup.as_view()),
    url(r'usergroups/add/manual/$', UserGroup.as_view()),
    url(r'usergroups/class/edit/$', UserGroup.as_view()),
    url(r'^instructors/$', InstructorList.as_view()),
    url(r'^users/quota/$', UserQuota.as_view()),
    url(r'^assignments/$', UserQuota.as_view()),
    url(r'^assignments/add/$', assignmentManage.as_view()),
    url(r'^assignments/launch/$', assignmentLaunch.as_view()),
    url(r'^assignments/launch/environment/$', assignmentLaunch.as_view()),
    ##url(r'^user/(?p<PK>\w+)$', UserSearch.as_view()),    
]
