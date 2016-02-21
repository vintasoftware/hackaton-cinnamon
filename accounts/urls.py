# coding: utf-8

from django.conf.urls import patterns, url

from accounts.views import RepoListView

urlpatterns = patterns('',
    url(r'^list/$', RepoListView.as_view(), name='list'),
)
