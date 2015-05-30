"""untitled URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from mentoring.views import *

urlpatterns = [
    url(r'^$', login_required(IndexView.as_view()), name='index'),

    url(r'^student/$', login_required(StudentView.as_view()), name='student-overview'),

    url(r'^placement/update/(?P<pk>\d+)/$', PlacementUpdateView.as_view(template_name='placement_form.html'),
        name='placement-update'),
    url(r'^placement/update/(?P<pk>\d+)/todo/$', PlacementUpdateView.as_view(template_name='placement_todo_form.html'),
        name='placement-update-todo'),
    url(r'^placement/preview/(?P<pk>\d+)/$', PlacementPreviewView.as_view(), name='placement-preview'),

    url(r'^thesis/mentoring-request/update/(?P<pk>\d+)/$',
        ThesisMentoringrequestUpdateView.as_view(template_name='thesis_mentoringrequest_form.html'),
        name='thesis-mentoringrequest-update'),
    url(r'^thesis/mentoring-request/update/(?P<pk>\d+)/todo/$',
        ThesisMentoringrequestUpdateView.as_view(template_name='thesis_mentoringrequest_todo_form.html'),
        name='thesis-mentoringrequest-update-todo'),
    url(r'^thesis/preview/(?P<pk>\d+)/$', ThesisPreviewView.as_view(), name='thesis-preview'),



    url(r'^tutor/$', TutorView.as_view(), name='tutor-overview'),
    url(r'^tutor/request/(?P<pk>\d+)/', TutorMentoringrequestView.as_view(), name='tutor-request')
]
