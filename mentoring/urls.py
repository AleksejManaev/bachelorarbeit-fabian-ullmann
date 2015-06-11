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

    url(r'^student/$', login_required(StudentUpdateView.as_view()), name='student-overview'),
    url(r'^student/settings/$', login_required(StudentSettingsView.as_view()), name='student-settings'),

    url(r'^placement/update/$', PlacementUpdateView.as_view(),
        name='placement-update'),
    url(r'^placement/update/todo/$',
        PlacementUpdateView.as_view(template_name='student/placement/placement_todo_form.html'),
        name='placement-update-todo'),
    url(r'^placement/preview/$', PlacementPreviewView.as_view(), name='placement-preview'),

    url(r'^thesis/mentoring-request/update/$',
        ThesisMentoringrequestUpdateView.as_view(),
        name='thesis-mentoringrequest-update'),
    url(r'^thesis/mentoring-request/update/todo/$',
        ThesisMentoringrequestUpdateView.as_view(
            template_name='student/thesis/mentoringrequest/mentoringrequest_todo_form.html'),
        name='thesis-mentoringrequest-update-todo'),

    url(r'^thesis/registration/update/$',
        ThesisRegistrationUpdateView.as_view(),
        name='thesis-registration-update'),
    url(r'^thesis/registration/update/todo/$',
        ThesisRegistrationUpdateView.as_view(template_name='student/registration/registration_todo_form.html'),
        name='thesis-registration-update-todo'),
    url(r'^thesis/registration/preview/$', ThesisRegistrationPDFPreview.as_view(), name='thesis-registration-preview'),
    url(r'^thesis/registration/pdf/$', ThesisRegistrationPDF.as_view(), name='thesis-registration-pdf'),
    url(r'^thesis/preview/$', ThesisPreviewView.as_view(), name='thesis-preview'),


    url(r'^tutor/$', TutorView.as_view(), name='tutor-overview'),
    url(r'^tutor/settings/$', login_required(TutorSettingsView.as_view()), name='tutor-settings'),
    url(r'^tutor/request/(?P<pk>\d+)/', TutorMentoringrequestView.as_view(), name='tutor-request'),
    url(r'^tutor/requests/', TutorMentoringrequestlistView.as_view(), name='tutor-requests'),
    url(r'^tutor/mentoring/(?P<pk>\d+)/', TutorMentoringView.as_view(), name='tutor-mentoring'),
    url(r'^tutor/mentorings/', TutorMentoringlistView.as_view(), name='tutor-mentorings'),
]
