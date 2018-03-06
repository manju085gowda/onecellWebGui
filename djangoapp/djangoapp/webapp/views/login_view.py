# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from webapp.forms import LoginForm
from ajax_forms.views import AjaxFormView
from django.views.generic import TemplateView
from webapp.models import *
from django.contrib.auth import authenticate
from django.contrib.auth import authenticate, login

def render_login_page(request):
    form_login = LoginForm()
    context = {'form_login':form_login}
    return render(request, 'login.html',context)


def sign_in(request):
    if(request.method == 'POST'):
        form_login = LoginForm(request.POST)
        if(form_login.is_valid()):
            username = form_login.cleaned_data['username']
            password = form_login.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/wizard/')
            # else:
            #
            #     #return redirect('/login/')

