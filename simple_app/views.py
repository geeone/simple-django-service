# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from django.contrib.auth.models import User
from models import CUser, Campaign, Domain, Server


@login_required(login_url='/login/')
def index(request):
    return redirect('/dashboard/')


def login_view(request):
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/')
    return render(request, 'login.html')


def signup_view(request):
    return render(request, 'sign_up.html')


def create_user(request):
    new_user = User.objects.create_user(
        request.POST['username'], request.POST['email'], request.POST['password'], is_active=0)
    CUser(user=new_user).save()
    return redirect('/')


@login_required(login_url='/login/')
def dashboard_view(request):
    user_info = CUser.objects.get(user=request.user.pk)
    total_domains = sum(map(lambda domains: len(domains),
                            [Domain.objects.filter(campaign=cp) for cp in Campaign.objects.filter(cuser=user_info.pk)]))
    total_campaigns = len(Campaign.objects.filter(cuser=request.user.pk))
    total_servers = len(Server.objects.all())
    return render(request, 'dashboard.html', {'user_info': user_info,
                                              'total_domains': total_domains,
                                              'total_campaigns': total_campaigns,
                                              'total_servers': total_servers})


@login_required(login_url='/login/')
def campaigns_view(request):
    user_info = CUser.objects.get(user=request.user.pk)
    campaigns = [{'id': cp.pk,
                  'name': cp.name,
                  'is_active': cp.is_active,
                  'domains_count': len(Domain.objects.filter(campaign=cp))} for cp in Campaign.objects.filter(cuser=user_info.pk)]
    return render(request, 'campaigns.html', {'current_user': user_info.user,
                                              'campaigns': campaigns})


@login_required(login_url='/login/')
def campaign_domains(request, campaign_id):
    user_info = CUser.objects.get(user=request.user.pk)
    if request.POST:
        return render(request, 'add_domain.html', {'current_user': user_info.user,
                                                   'campaign_id': campaign_id})
    else:
        current_campaign = Campaign.objects.get(pk=campaign_id, cuser=user_info.pk)
        domains = Domain.objects.filter(campaign=campaign_id)
        return render(request, 'domains.html', {'current_user': user_info.user,
                                                'current_campaign': current_campaign,
                                                'domains': domains})


def add_domain(request, campaign_id):
    is_used = request.POST.get('is_used')
    is_active = request.POST.get('is_active')
    if not is_used:
        is_used = 0
    if not is_active:
        is_active = 0
    d = Domain(name=request.POST.get('name'), is_used=is_used, is_active=is_active)
    d.save()
    c = Campaign.objects.get(pk=campaign_id)
    c.domain_list.add(d)
    previous_url = request.META.get('HTTP_REFERER')
    print previous_url
    return redirect(previous_url)


def campaign_server(request, campaign_id):
    current_user = request.user
    current_campaign = Campaign.objects.get(pk=campaign_id)
    server_info = Server.objects.get(campaign=campaign_id)
    return render(request, 'server.html', {'current_user': current_user,
                                           'current_campaign': current_campaign,
                                           'server_info': server_info})


@login_required(login_url='/login/')
def settings_view(request):
    return redirect("/settings/rotator/")


@login_required(login_url='/login/')
def rotator_settings(request):
    user_info = CUser.objects.get(user=request.user.pk)
    return render(request, 'rotator_settings.html', {'user_info': user_info})


@login_required(login_url='/login/')
def party_keys_settings(request):
    user_info = CUser.objects.get(user=request.user.pk)
    return render(request, 'party_keys_settings.html', {'user_info': user_info})


@login_required(login_url='/login/')
def settings_save(request):
    if request.POST:
        auto_rotate_minutes = request.POST.get('auto_rotate_minutes')
        if auto_rotate_minutes:
            is_auto_rotate = request.POST.get('is_auto_rotate')
            if not is_auto_rotate:
                is_auto_rotate = 0
            CUser.objects.filter(pk=request.user.pk).update(is_auto_rotate=is_auto_rotate,
                                                            auto_rotate_minutes=auto_rotate_minutes)
        else:
            CUser.objects.filter(pk=request.user.pk).update(do_key=request.POST.get('do_key'),
                                                            vu_key=request.POST.get(
                                                                'vu_key'),
                                                            rc_key=request.POST.get(
                                                                'rc_key'),
                                                            nc_key=request.POST.get(
                                                                'nc_key'),
                                                            fn_key=request.POST.get('fn_key'))
        previous_url = request.META.get('HTTP_REFERER')
        return redirect(previous_url)


@login_required(login_url='/login/')
def campaigns_save(request, campaign_id):
    if request.POST:
        Server.objects.filter(pk=request.POST['current_server']
                              ).update(name=request.POST['server_name'],
                                       server_ip=request.POST['server_ip'],
                                       server_password=request.POST['server_psswrd'])
        previous_url = request.META.get('HTTP_REFERER')
        return redirect(previous_url)


def _pause_campaigns(request, campaign_id):
    previous_url = request.META.get('HTTP_REFERER')
    Campaign.objects.filter(pk=campaign_id).update(is_active=0)
    return redirect(previous_url)


def _resume_campaigns(request, campaign_id):
    previous_url = request.META.get('HTTP_REFERER')
    Campaign.objects.filter(pk=campaign_id).update(is_active=1)
    return redirect(previous_url)


def _drop_campaigns(request, campaign_id):
    previous_url = request.META.get('HTTP_REFERER')
    Campaign.objects.get(pk=campaign_id).delete()
    return redirect(previous_url)


def _pause_domains(request, domain_id):
    previous_url = request.META.get('HTTP_REFERER')
    Domain.objects.filter(pk=domain_id).update(is_active=0)
    return redirect(previous_url)


def _resume_domains(request, domain_id):
    previous_url = request.META.get('HTTP_REFERER')
    Domain.objects.filter(pk=domain_id).update(is_active=1)
    return redirect(previous_url)


def _drop_domains(request, domain_id):
    previous_url = request.META.get('HTTP_REFERER')
    Domain.objects.get(pk=domain_id).delete()
    return redirect(previous_url)
