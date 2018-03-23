# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from time import gmtime, strftime
from django.utils.crypto import get_random_string
from models import *
import bcrypt
# Create your views here.

def index(request):
    context = {
        "users" : User.objects.all()
    }
    return render(request,'djangoBeltExam_app/index.html',context)

def register(request):
    errors = User.objects.register_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:
        User.objects.create(
            first_name = str(request.POST['first_name']),
            last_name = str(request.POST['last_name']),
            email = str(request.POST['email']),
            password = str(bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())),
            bday = str(request.POST['last_name'])
            )
        user = User.objects.get(email = request.POST['email'])
        request.session['user_id'] = user.id
    return redirect('/list_quotes')


def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:
        user = User.objects.get(email = request.POST['email'])
        request.session['user_id'] = user.id
    return redirect('/list_quotes')

def list_quotes(request):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        "user" : User.objects.get(id=request.session['user_id']),
        "favorites" : Quote.objects.filter(liked_users = User.objects.get(id = request.session['user_id'])),
        "quotes" : Quote.objects.exclude(liked_users = User.objects.get(id = request.session['user_id']))
    }
    return render(request,'djangoBeltExam_app/list_quotes.html',context)

def new_quote(request):
    errors = Quote.objects.quote_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/list_quotes')
    else:
        new_quote = Quote.objects.create(
            quoted_by = str(request.POST['quoted_by']),
            message = str(request.POST['message']),
            contributer = User.objects.get(id=request.session['user_id']),
            )
    return redirect('/list_quotes')

def add_like(request, id):
    liked = Quote.objects.get(id = id)
    liked.liked_users.add(User.objects.get(id=request.session['user_id']))
    return redirect('/list_quotes')


def remove_like(request, id):
    remove = Quote.objects.get(id=id)
    remove.liked_users.remove(User.objects.get(id=request.session['user_id']))
    return redirect('/list_quotes')

def view_user(request, id):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        "user" : User.objects.get(id=id),
        "quotes" : Quote.objects.filter(contributer = User.objects.get(id=id)),
        "count" : len(Quote.objects.filter(contributer = User.objects.get(id=id)))
    }
    return render(request,'djangoBeltExam_app/view_user.html',context)














