from datetime import datetime
from time import sleep

import pytz
from django.contrib.auth import login, get_user_model
from django.shortcuts import render, redirect

from .models import User
from accounts.forms import RegisterForm, LoginForm
from django.contrib.auth import logout


User = get_user_model()


def registerpage(request):
    form = RegisterForm(request.POST or None)

    if request.POST and form.is_valid():
        user = form.save()
        if user:
            return redirect('/users/')

    context = {
        'form': form,
    }

    return render(request, "auth/register.html", context)


def loginpage(request):
    form = LoginForm(request.POST or None)
    if request.POST and form.is_valid():
        user = form.login(request)
        if user:
            login(request, user)
            if not request.user.loginTime:
                qs = User.objects.filter(email=request.user)
                qs.update(loginTime=datetime.today().replace(tzinfo=pytz.UTC), logoutTime=datetime.today().replace(tzinfo=pytz.UTC))
            return redirect('homepage')
    context = {
        "form": form
    }
    return render(request, "auth/login.html", context)


def logout_view(request):
    username = loginpage(request)
    if username:

        if not request.user.logoutTime:
            qs = User.objects.filter(email=request.user)
            qs.update(logoutTime=datetime.today().replace(tzinfo=pytz.UTC))

        if request.user.logoutTime:
            qs = User.objects.filter(email=request.user)
            qs.update(logoutTime=datetime.today().replace(tzinfo=pytz.UTC))
        # sleep(10)
        abc = request.user.loginTime
        # efg = datetime.time(request.user.logoutTime)
        test = request.user.logoutTime
        total = test - abc
        qs = User.objects.filter(email=request.user)
        qs.update(totalDays=total.days)
        logout(request)
        return redirect('loginpage')