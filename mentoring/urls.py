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

    url(r'^student/$', login_required(StudentIndexView.as_view()), name='student-index'),
    url(r'^student/settings/$', login_required(StudentSettingsFormView.as_view()), name='student-settings'),
    url(r'^student/placement/$', login_required(StudentFormView.as_view()), name='student-placement'),
    url(r'^student/placement/update/$', StudentPlacementFormView.as_view(), name='student-placement-update'),

    url(r'^tutor/placement/update/(?P<pk>\d+)/$', login_required(TutorUpdatePlacementView.as_view()), name='tutor-placement-update'),
    url(r'^tutor/placement/(?P<pk>\d+)/$', TutorPlacementView.as_view(template_name='tutor_placement_details.html'), name='placement-details'),
    url(r'^tutor/$', TutorView.as_view(), name='tutor-index'),
    url(r'^tutor/settings/$', login_required(TutorSettingsFormView.as_view()), name='tutor-settings'),

    url(r'^comments/placement/(?P<pk>\d+)$', login_required(PlacementCommentsView.as_view()), name='placements-comments'),
    url(r'^comments/placement/toggleprivacy$', login_required(togglePrivacy), name='placements-comments'),
]
