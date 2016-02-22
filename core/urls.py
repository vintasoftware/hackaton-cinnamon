"""Yacht URL Configuration

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
from django.conf.urls import include, url
from django.contrib.auth.views import logout
from django.contrib import admin

from core.views import LandingPageView, LoadingTemplateView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', LandingPageView.as_view(), name='home'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^repo/', include('accounts.urls', namespace='repo')),
    url(r'^logout/$', logout, name='logout', kwargs={'next_page': '/'}),
    url(r'^loading/$', LoadingTemplateView.as_view(), name='loading'),

    # url(r'^api/v1/', include('bikeways.endpoints_urls')),
]
