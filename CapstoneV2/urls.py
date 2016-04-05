"""CapstoneV2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from chfapp.views import home, userLogin, newUserLogin, activityDashboard, activityPage, activity
from chfapp.views import newEventForm, newActivityForm, deleteEvent, editEvent, deleteActivity, newAdmin
from chfapp.views import editActivity, newSceneSetForm, endSession, deleteInactiveSessions, joinEvent
from chfapp.views import eventDashboard, editScene, editSceneOption, deleteSceneOption, quickStart

#where URLS are created; none have been created for userdashboard yet
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', 'chfapp.views.home', name='home'),
    url(r'^userLogin/$', 'chfapp.views.userLogin', name='userLogin'),
    url(r'^contact/$', 'chfapp.views.contact', name='contact'),
    url(r'^newAdmin/$', 'chfapp.views.newAdmin', name='newAdmin'),
    url(r'^newUserLogin/$', 'chfapp.views.newUserLogin', name='newUserLogin'),
    url(r'^activity/(\d+)/$', 'chfapp.views.activity', name='activity'),
    url(r'^activityDashboard/(\d+)/$', 'chfapp.views.activityDashboard', name='activityDashboard'),
    url(r'^activityPage/(\d+)/$', 'chfapp.views.activityPage',name='activityPage'),
    url(r'^eventDashboard/$', 'chfapp.views.eventDashboard', name='eventDashboard'),    
    url(r'^activityPage/(\d+)/(\d+)/$', 'chfapp.views.activityPage',name='activityPage2'),
    url(r'^eventDashboard/(\d+)/$', 'chfapp.views.eventDashboard', name='eventDashboard2'),    
    url(r'^createEvent/$', 'chfapp.views.newEventForm', name='createEvent'),
    url(r'^adminDashboard/$', 'chfapp.views.adminDashboard', name='adminDashboard'),
    url(r'^adminDashboard/(\d+)/$', 'chfapp.views.adminDashboard', name='adminDashboard'),
    url(r'^createActivity/(\d+)/$', 'chfapp.views.newActivityForm', name='createActivity'),
    url(r'^deleteEvent/(\d+)/$', 'chfapp.views.deleteEvent', name='deleteEvent'),
    url(r'^editEvent/(\d+)/$', 'chfapp.views.editEvent', name='editEvent'),
    url(r'^editActivity/(\d+)/$', 'chfapp.views.editActivity', name='editActivity'),
    url(r'^deleteActivity/(\d+)/$', 'chfapp.views.deleteActivity', name='deleteActivity'),
    url(r'^createSceneSet/(\d+)/$', 'chfapp.views.newSceneSetForm', name='createSceneSet'),
    url(r'^activity/(\d+)/$', 'chfapp.views.newSceneOptionSetForm', name='newSceneOptionSet'),
    url(r'^newNextSceneSet/(\d+)/$', 'chfapp.views.newNextSceneSetForm', name='newNextSceneSet'),
    url(r'^editScene/(\d+)/$', 'chfapp.views.editScene', name='editScene'),
    url(r'^deleteScene/(\d+)/$', 'chfapp.views.deleteScene', name='deleteScene'),
    url(r'^editSceneOption/(\d+)/$', 'chfapp.views.editSceneOption', name='editSceneOption'),
    url(r'^deleteSceneOption/(\d+)/$', 'chfapp.views.deleteSceneOption', name='deleteSceneOption'),
    url(r'^endSession/(\d+)/$', 'chfapp.views.endSession', name='endSession'),
    url(r'^deleteInactiveSessions/(\d+)/$', 'chfapp.views.deleteInactiveSessions', name='deleteInactiveSessions'),
    url(r'^joinEvent/(\d+)/$', 'chfapp.views.joinEvent', name='joinEvent'),    
    url(r'^createScenePath/(\d+)/$', 'chfapp.views.newSceneOptionSetForm', name='createScenePath'),
    url(r'^quickStart/$', 'chfapp.views.quickStart', name='quickStart'),
    url(r'^logout/$', 'chfapp.views.logout', name='logout')

] + static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)