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
from chfapp.views import newEventForm, newActivityForm, deleteEvent, editEvent, deleteActivity
from chfapp.views import editActivity, newSceneSetForm, newSceneOptionSetForm
from chfapp.views import eventDashboard, editScene

#where URLS are created; none have been created for userdashboard yet
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', 'chfapp.views.home', name='home'),
    url(r'^userLogin/$', 'chfapp.views.userLogin', name='userLogin'),
    url(r'^contact/$', 'chfapp.views.contact', name='contact'),
    url(r'^newUserLogin/$', 'chfapp.views.newUserLogin', name='newUserLogin'),
    url(r'^activity/(\d+)/$', 'chfapp.views.activity', name='activity'),
    url(r'^activityDashboard/$', 'chfapp.views.activityDashboard', name='activityDashboard'),
    url(r'^activityPage/(\d+)/$', 'chfapp.views.activityPage',name='activityPage'),
    url(r'^activityPage/(\d+)/(\d+)/$', 'chfapp.views.activityPage',name='activityPage2'),
    url(r'^eventDashboard/$', 'chfapp.views.eventDashboard', name='eventDashboard'),    
    url(r'^createEvent/$', 'chfapp.views.newEventForm', name='createEvent'),
    url(r'^adminDashboard/$', 'chfapp.views.adminDashboard', name='adminDashboard'),
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
    url(r'^createScenePath/(\d+)/$', 'chfapp.views.newSceneOptionSetForm', name='createScenePath')

] + static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)