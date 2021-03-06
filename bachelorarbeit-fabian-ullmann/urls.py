# -*- coding: utf-8 -*-
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
from account.views import LoginView
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.core.urlresolvers import reverse_lazy

urlpatterns = [
                  url(r'^accounts/login/$', LoginView.as_view(template_name='ldap_login.html'), name='login'),
                  url(r'^accounts/logout/$',
                      auth_views.logout,
                      {'next_page': reverse_lazy('index')},
                      name='logout'),
                  url(r'^', include('mentoring.urls')),
                  url(r'^admin/', include(admin.site.urls)),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler500 = 'mentoring.views.handler500'
handler404 = 'mentoring.views.handler500'
