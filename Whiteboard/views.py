from datetime import datetime, time, date, timedelta

import pytz
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model

User = get_user_model()


def home_page(request):

    if request.user.is_authenticated:
        print(request.user.totalDays) #request.user.totalDays mo lng para mapasa mo sa frontend each object gets mo na nun yon
        return redirect('coursepage')
    else:

        return redirect('loginpage')


def my_info_page(request):
    if request.user.is_authenticated:
        return render(request, "auth/infopage.html")
    else:
        return redirect('loginpage')


def list_user(request):
    if request.GET.get('search'):
        search = request.GET.get('search')
        users = User.objects.all().filter(email__contains=search)
    else:
        users = User.objects.all()

    context = {
        'users': users
    }
    return render(request, 'auth/list_user.html', context)


def update(request, id):
    user = User.objects.get(id=id)
    context = {
        'user': user
    }
    return render(request, 'auth/update.html', context)


def delete(request, id):
    user = User.objects.get(id=id)
    user.delete()
    return redirect('list_user')


def update_record(request, id):
    newEmail = request.POST['email']
    newFirstName = request.POST['first_name']
    newLastName = request.POST['last_name']
    user = User.objects.get(id=id)
    user.email = newEmail
    user.first_name = newFirstName
    user.last_name = newLastName
    user.save()
    return redirect('list_user')

