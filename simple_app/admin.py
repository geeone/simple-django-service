# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import Server, Domain, Campaign, CUser

# Register your models here.


class ServerAdmin(admin.ModelAdmin):
    list_display = ['name', 'server_type', 'server_ip', 'server_username', 'server_password']

admin.site.register(Server, ServerAdmin)


class DomainAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_used', 'is_active']

admin.site.register(Domain, DomainAdmin)


class CampaignAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'domains', 'server']

    def domains(self, obj):
        return "\n".join([p.name for p in obj.domain_list.all()])

admin.site.register(Campaign, CampaignAdmin)


class CUserAdmin(admin.ModelAdmin):
    list_display = ['user', 'subtype', 'do_key', 'vu_key', 'rc_key', 'nc_key', 'fn_key', 'is_auto_rotate', 'auto_rotate_minutes', 'rotator_running', 'campaigns']

    def campaigns(self, obj):
        return "\n".join([p.name for p in obj.campaign_list.all()])

admin.site.register(CUser, CUserAdmin)
