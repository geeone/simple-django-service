"""simple_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin
from simple_app import views


settings_pattern = [
    url(r'^$', views.settings_view),
    url(r'^rotator/$', views.rotator_settings),
    url(r'^party_keys/$', views.party_keys_settings),
    url(r'^save_settings/$', views.settings_save),
]

campaigns_pattern = [
    url(r'^$', views.campaigns_view),
    url(r'^(?P<campaign_id>\d+)/$', views.campaign_domains),
    url(r'^(?P<campaign_id>\d+)/domains/$', views.campaign_domains),
    url(r'^(?P<campaign_id>\d+)/server/$', views.campaign_server),
    url(r'^(?P<campaign_id>\d+)/add_domain/$', views.add_domain),
    url(r'^(?P<campaign_id>\d+)/server/save_settings/$', views.campaigns_save),
    url(r'^(?P<campaign_id>\d+)/pause/$', views._pause_campaigns),
    url(r'^(?P<campaign_id>\d+)/resume/$', views._resume_campaigns),
    url(r'^(?P<campaign_id>\d+)/drop/$', views._drop_campaigns),
]

domains_pattern = [
    url(r'^(?P<domain_id>\d+)/pause/$', views._pause_domains),
    url(r'^(?P<domain_id>\d+)/resume/$', views._resume_domains),
    url(r'^(?P<domain_id>\d+)/drop/$', views._drop_domains),
]

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^$', views.index),
    url(r'^login/$', views.login_view),
    url(r'^sign_up/$', views.signup_view),
    url(r'^create_user/$', views.create_user),
    url(r'^dashboard/$', views.dashboard_view),
    url(r'^settings/', include(settings_pattern)),
    url(r'^campaigns/', include(campaigns_pattern)),
    url(r'^domains/', include(domains_pattern)),
]
