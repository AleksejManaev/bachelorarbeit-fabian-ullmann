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

from .views import *

urlpatterns = [
    url(r'^form/$', MaterialFormView.as_view()),
    url(r'^formset/$', MaterialFormsetView.as_view()),
    url(r'^form-manual/$', MaterialFormManualView.as_view()),

    url(r'^form/todo/$', MaterialFormView.as_view(template_name='material_todo_form.html')),
    url(r'^formset/todo/$', MaterialFormsetView.as_view(template_name='material_todo_manual.html')),
    url(r'^form-manual/todo/$', MaterialFormManualView.as_view()),

    url(r'^update/(?P<pk>\d+)/', MaterialUpdateView.as_view(
        model=MaterializeTestModel,
        fields=['text', 'date', 'message', 'email', 'password', 'file']), name='update'),
    url(r'^create/todo/$', CreateView.as_view(
        model=MaterializeTestModel,
        fields=['text', 'date', 'message', 'password', 'email', 'file'],
        template_name='material_todo_form.html')),
]
