# -*- coding: utf-8 -*-
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render_to_response,render,get_object_or_404  
from django.http import HttpResponse, HttpResponseRedirect  
from django.contrib.auth.models import User  
from django.contrib import auth
from django.contrib import messages
from django.template.context import RequestContext
from django.shortcuts import redirect
from django.forms.formsets import formset_factory
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse
from bootstrap_toolkit.widgets import BootstrapUneditableInput
from django.contrib.auth.decorators import login_required

from forms import LoginForm




def index(request):
    return redirect(reverse(login))
    
def login(request):

    if request.method == 'GET':
        if request.user.is_authenticated():
            return render_to_response('base.html', RequestContext(request))
        else:
            form = LoginForm()
            return render_to_response('user/login.html', RequestContext(request, {'form': form,}))
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
                return render_to_response('base.html', RequestContext(request))
            else:
                return render_to_response('user/login.html', RequestContext(request, {'form': form,'password_is_wrong':True, 'errors': u'登录失败，请检查登录信息'}))
        else:
            return render_to_response('user/login.html', RequestContext(request, {'form': form, 'input_is_wrong':True, 'errors': u'请正确输入登录信息'}))
 
 
 
@login_required          
def dashboard(request):
    return render_to_response('base.html')


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse(login))