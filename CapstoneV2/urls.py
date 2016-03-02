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

from chfapp.views import home, userLogin, newUserLogin, activityDashboard, activityStart, activityPage

#where URLS are created; none have been created for userdashboard yet
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', 'chfapp.views.home', name='home'),
    url(r'^userLogin/$', 'chfapp.views.userLogin', name='userLogin'),
    url(r'^contact/$', 'chfapp.views.contact', name='contact'),
    url(r'^newUserLogin/$', 'chfapp.views.newUserLogin', name='newUserLogin'),
    url(r'^activityDashboard/$', 'chfapp.views.activityDashboard', name='activityDashboard'),
    # url(r'^activityStart/(\d)/$', 'chfapp.views.activityStart',name='activityStart'),
    url(r'^activityPage/(\d+)/$', 'chfapp.views.activityPage',name='activityPage'),
    url(r'^activityPage/(\d+)/(\d+)/$', 'chfapp.views.activityPage',name='activityPage2')
    #url() for when admin form is created/added to newUserLogin
    #url() for when event, activity is created/added

] + static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)