# coding: utf-8

from django.conf.urls import patterns, url

from accounts.views import RepoListView, RepoCreateView, RepoDeleteView

urlpatterns = patterns('',
    url(r'^list/$', RepoListView.as_view(), name='list'),
    url(r'^create/$', RepoCreateView.as_view(), name='create'),
    url(r'^delete/$', RepoDeleteView.as_view(), name='delete'),
)
