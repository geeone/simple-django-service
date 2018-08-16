# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Server(models.Model):
    name = models.CharField(max_length=100)
    server_type = models.CharField(max_length=30)
    server_ip = models.CharField(max_length=50)
    server_username = models.CharField(max_length=100)
    server_password = models.CharField(max_length=100)

    def __unicode__(self):
        return unicode(self.name)


class Domain(models.Model):
    name = models.CharField(max_length=100)
    is_used = models.IntegerField(default=0)
    is_active = models.IntegerField(default=0)

    def __unicode__(self):
        return unicode(self.name)


class Campaign(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.IntegerField(default=0)
    domain_list = models.ManyToManyField(Domain)
    server = models.ForeignKey(Server)

    def __unicode__(self):
        return unicode(self.name)


class CUser(models.Model):
    user = models.OneToOneField(User, null=True, on_delete = models.CASCADE)
    subtype = models.IntegerField(default=0)
    do_key = models.CharField(max_length=100, null=True, blank=True)
    vu_key = models.CharField(max_length=100, null=True, blank=True)
    rc_key = models.CharField(max_length=100, null=True, blank=True)
    nc_key = models.CharField(max_length=100, null=True, blank=True)
    fn_key = models.CharField(max_length=100, null=True, blank=True)
    is_auto_rotate = models.IntegerField(default=0)
    auto_rotate_minutes = models.IntegerField(default=0)
    rotator_running = models.IntegerField(default=0)
    campaign_list = models.ManyToManyField(Campaign)

    def __unicode__(self):
        return unicode(self.user)
