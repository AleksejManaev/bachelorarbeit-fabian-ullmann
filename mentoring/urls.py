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
    url(r'^student/placement/update/todo/$',
        StudentPlacementFormView.as_view(template_name='student_placement_form_todo.html'),
        name='student-placement-update-todo'),
    url(r'^student/placement/(?P<pk>\d+)/$', StudentPlacementIndexView.as_view(), name='student-placement-preview'),
    url(r'^student/placement/create/$', studentPlacementCreate, name='student-placement-create'),
    url(r'^student/placement/(?P<pk>\d+)/editable/$', studentPlacementEditable, name='student-placement-editable'),
    url(r'^student/placement/(?P<pk>\d+)/delete/$', studentPlacementDelete, name='student-placement-delete'),

    url(r'^student/theses/$', StudentThesisListView.as_view(), name='student-theses'),
    url(r'^student/thesis/preview/$', StudentThesisIndexView.as_view(), name='student-thesis-preview'),
    url(r'^student/thesis/create/$', studentThesisCreate, name='student-thesis-create'),
    url(r'^student/thesis/(?P<pk>\d+)/editable/$', studentThesisEditable, name='student-thesis-editable'),
    url(r'^student/thesis/(?P<pk>\d+)/delete/$', studentThesisDelete, name='student-thesis-delete'),
    url(r'^student/thesis/request/update/$', StudentThesisMentoringrequestFormView.as_view(),
        name='student-thesis-mentoringrequest-update'),
    url(r'^student/thesis/request/update/todo/$',
        StudentThesisMentoringrequestFormView.as_view(template_name='student_thesis_mentoringrequest_form_todo.html'),
        name='student-thesis-mentoringrequest-update-todo'),
    url(r'^student/thesis/request/preview/$', StudentThesisMentoringrequestView.as_view(),
        name='student-thesis-mentoringrequest-preview'),

    url(r'^student/thesis/registration/update/$', StudentThesisRegistrationFormView.as_view(),
        name='student-thesis-registration-update'),
    url(r'^student/thesis/registration/update/todo/$',
        StudentThesisRegistrationFormView.as_view(template_name='student_thesis_registration_form_todo.html'),
        name='student-thesis-registration-update-todo'),

    url(r'^student/thesis/documents/update/$', StudentThesisDocumentsFormView.as_view(),
        name='student-thesis-documents-update'),
    url(r'^student/thesis/documents/update/todo/$',
        StudentThesisDocumentsFormView.as_view(template_name='student_thesis_documents_form_todo.html'),
        name='student-thesis-documents-update-todo'),
    url(r'^student/thesis/documents/preview/$', StudentThesisIndexView.as_view(),
        name='student-thesis-documents-preview'),
    url(r'^download/(?P<pk>\d+)/(?P<documenttype>\w+)$', login_required(DownloadView.as_view()), name='download'),
    url(r'^tutor/placement/(?P<pk>\d+)/$', TutorPlacementView.as_view(template_name='tutor_placement_details.html'), name='placement-details'),
    url(r'^tutor/placement/update/(?P<pk>\d+)/$', login_required(TutorUpdatePlacementView.as_view()), name='tutor-placement-update'),
    url(r'^tutor/$', TutorView.as_view(), name='tutor-index'),
    url(r'^tutor/(?P<order_by>)$', TutorView.as_view(), name='order-by'),
    url(r'^tutor/settings/$', login_required(TutorSettingsFormView.as_view()), name='tutor-settings'),
    url(r'^tutor/placements/$', TutorPlacementListView.as_view(), name='tutor-placements'),
    url(r'^tutor/placements/course/(?P<pk>\d+)/$', TutorPlacementCourseView.as_view(), name='tutor-placement-course'),
    url(r'^tutor/placements/course/(?P<pk>\d+)/registrations/$', TutorPlacementCourseRegistrationView.as_view(),
        name='tutor-placement-course-registrations'),
    url(r'^tutor/placements/course/(?P<pk>\d+)/registrations/confirmed$',
        TutorPlacementCourseRegistrationView.as_view(), {'confirmed': True},
        name='tutor-placement-course-registrations-confirmed'),
    url(r'^tutor/placements/course/(?P<pk>\d+)/registrations/notconfirmed$',
        TutorPlacementCourseRegistrationView.as_view(), {'confirmed': False},
        name='tutor-placement-course-registrations-notconfirmed'),
    url(r'^tutor/placements/course/(?P<pk>\d+)/addevent/$', TutorPlacementCourseEventView.as_view(),
        name='tutor-placement-course-addevent'),
    url(r'^tutor/placements/course/(?P<pk>\d+)/editevent/$', TutorPlacementCourseEventFormView.as_view(),
        name='tutor-placement-course-editevent'),
    url(r'^tutor/placements/course/(?P<pk>\d+)/deleteevent/(?P<ev>\d+)/$', tutorPlacementCourseEventDelete,
        name='tutor-placement-course-deleteevent'),
    url(r'^tutor/placement/(?P<pk>\d+)/$', TutorPlacementView.as_view(), name='tutor-placement-preview'),
    url(r'^tutor/placement/(?P<pk>\d+)/confirm$', tutorPlacementConfirm, name='tutor-placement-confirm'),

    url(r'^tutor/request/(?P<pk>\d+)/', TutorMentoringRequestFormView.as_view(), name='tutor-request'),
    url(r'^tutor/requests/', TutorMentoringRequestListView.as_view(), name='tutor-requests'),
    url(r'^tutor/mentorings/', TutorMentoringListView.as_view(), name='tutor-mentorings'),
    url(r'^tutor/mentoring/(?P<pk>\d+)/$', TutorMentoringFormView.as_view(), name='tutor-mentoring'),
    url(r'^tutor/mentoring/(?P<pk>\d+)/colloquium/$', TutorMentoringColloquiumFormView.as_view(),
        name='tutor-mentoring-colloquium'),
    url(r'^tutor/mentoring/(?P<pk>\d+)/report/$', TutorMentoringReportFormView.as_view(),
        name='tutor-mentoring-report'),

    url(r'^thesis/registration/(?P<pk>\d+)/preview/$', BothThesisRegistrationPDFDownloadPreview.as_view(),
        name='thesis-registration-preview'),
    url(r'^thesis/registration/(?P<pk>\d+)/pdf/$', BothThesisRegistrationPDFDownload.as_view(),
        name='thesis-registration-pdf'),
    url(r'^thesis/registration/(?P<pk>\d+)/examinationboard/', BothThesisExaminationboardFormView.as_view(),
        name='thesis-registration-examinationboard'),
    url(r'^thesis/preview/$', StudentThesisIndexView.as_view(), name='thesis-preview'),
]
