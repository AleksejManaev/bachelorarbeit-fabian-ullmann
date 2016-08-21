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
    url(r'^student/placement/$', login_required(StudentPlacementFormView.as_view()), name='student-placement'),
    url(r'^student/placement/update/$', login_required(StudentPlacementFormView.as_view()), name='student-placement-update'),
    url(r'^student/placementseminarentrylist/$', login_required(StudentPlacementSeminarEntryView.as_view()), name='student-placement-seminar-entry-list'),
    url(r'^student/thesisseminarentrylist/$', login_required(StudentThesisSeminarEntryView.as_view()), name='student-thesis-seminar-entry-list'),
    url(r'^student/thesis/$', login_required(StudentThesisFormView.as_view()), name='student-thesis'),
    url(r'^student/completed_theses/$', login_required(StudentCompletedThesesView.as_view()), name='student-completed-theses'),

    url(r'^tutor/placement/update/(?P<pk>\d+)/$', login_required(TutorUpdatePlacementView.as_view()), name='tutor-placement-update'),
    url(r'^tutor/placement/(?P<pk>\d+)/$', login_required(TutorPlacementView.as_view()), name='placement-details'),
    url(r'^tutor/placement/document/(?P<pk>\d+)/$', login_required(generate_placement_document), name='placement-document'),
    url(r'^tutor/thesis/document/(?P<pk>\d+)/$', login_required(generate_thesis_document), name='thesis-document'),
    url(r'^tutor/thesis/update/(?P<pk>\d+)/$', login_required(TutorUpdateThesisView.as_view()), name='tutor-thesis-update'),
    url(r'^tutor/thesis/(?P<pk>\d+)/$', login_required(TutorThesisView.as_view()), name='thesis-details'),
    url(r'^tutor/$', TutorView.as_view(), name='tutor-index'),
    url(r'^tutor/settings/$', login_required(TutorSettingsFormView.as_view()), name='tutor-settings'),
    url(r'^tutor/placementseminar/$', login_required(PlacementSeminarListView.as_view()), name='placement-seminar-list'),
    url(r'^tutor/placementseminar/create$', login_required(PlacementSeminarCreateView.as_view()), name='placement-seminar-create'),
    url(r'^tutor/placementseminar/(?P<pk>\d+)/$', login_required(PlacementSeminarUpdateView.as_view()), name='placement-seminar-update'),
    url(r'^tutor/placementseminarentry/create$', login_required(PlacementSeminarEntryCreateView.as_view()), name='placement-seminar-entry-create'),
    url(r'^tutor/placementseminarentry/process$', login_required(PlacementSeminarEntryProcessView.as_view()), name='placement-seminar-entry-process'),
    url(r'^tutor/placementseminarentry/(?P<pk>\d+)/delete$', login_required(PlacementSeminarEntryDeleteView.as_view()), name='placement-seminar-entry-delete'),
    url(r'^tutor/posters$', login_required(PostersView.as_view()), name='posters-index'),
    url(r'^tutor/posters/update/(?P<pk>\d+)$', login_required(PosterUpdateView.as_view()), name='tutor-poster-update'),

    url(r'^tutor/thesisseminar/$', login_required(ThesisSeminarView.as_view()), name='thesis-seminar-list'),

    url(r'^tutor/thesisbachelorseminar/(?P<pk>\d+)/$', login_required(BachelorSeminarUpdateView.as_view()), name='bachelor-seminar-update'),
    url(r'^tutor/thesisbachelorseminar/create$', login_required(BachelorSeminarCreateView.as_view()), name='bachelor-seminar-create'),
    url(r'^tutor/thesisbachelorseminarentry/process$', login_required(BachelorSeminarEntryProcessView.as_view()), name='bachelor-seminar-entry-process'),
    url(r'^tutor/thesisbachelorseminarentry/create$', login_required(BachelorSeminarEntryCreateView.as_view()), name='bachelor-seminar-entry-create'),
    url(r'^tutor/thesisbachelorseminarentry/(?P<pk>\d+)/delete$', login_required(BachelorSeminarEntryDeleteView.as_view()), name='bachelor-seminar-entry-delete'),

    url(r'^tutor/thesismasterseminar/(?P<pk>\d+)/$', login_required(MasterSeminarUpdateView.as_view()), name='master-seminar-update'),
    url(r'^tutor/thesismasterseminar/create$', login_required(MasterSeminarCreateView.as_view()), name='master-seminar-create'),
    url(r'^tutor/thesismasterseminarentry/process$', login_required(MasterSeminarEntryProcessView.as_view()), name='master-seminar-entry-process'),
    url(r'^tutor/thesismasterseminarentry/create$', login_required(MasterSeminarEntryCreateView.as_view()), name='master-seminar-entry-create'),
    url(r'^tutor/thesismasterseminarentry/(?P<pk>\d+)/delete$', login_required(MasterSeminarEntryDeleteView.as_view()), name='master-seminar-entry-delete'),

    url(r'^comments/abstractwork/(?P<pk>\d+)$', login_required(CommentsView.as_view()), name='comments'),
    url(r'^comments/abstractwork/toggleprivacy$', login_required(togglePrivacy), name='toggle-privacy'),
]
