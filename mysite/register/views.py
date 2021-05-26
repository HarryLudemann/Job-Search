
from django.contrib.auth.forms import UserChangeForm
from django.http import request
from django.shortcuts import render, redirect
from .forms import RegisterForm, EditProfile, OccupationForm
from django.contrib.auth.models import User
from django.views import generic
from register.models import Occupation

#Checks if employer
def CheckEmployer(response):
    obj = Occupation.objects.all()
    if (obj.filter(userid=response.user.id).exists()): 
        obj = obj.filter(userid=response.user.id)
        for item in obj:
            if (item.employer == True):
                return True
            else:
                return False
    else:
        return False

# Create your views here.
def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
        return redirect("/")
    else:
        form = RegisterForm()

    return render(response, "register/register.html", {"form":form})


def editprofile(response):
    # user = User.objects.get(username = response.user.username)
    if response.method == "POST":
        form = EditProfile(response.POST, instance=response.user)
        if form.is_valid():
            form.save()
            
        obj = Occupation.objects.all()
        if (obj.filter(userid=response.user.id).exists()):
            obj.filter(userid=response.user.id).delete()

        occupationform = OccupationForm(response.POST)
        if occupationform.is_valid():
            obj = Occupation(userid=response.user.id, student=occupationform.cleaned_data["student"], employer=occupationform.cleaned_data["employer"])
            obj.save()
        return redirect("/")
    else:
        form = EditProfile(instance=response.user)
        obj = Occupation.objects.all()
        if (obj.filter(userid=response.user.id).exists()):
            obj = obj.filter(userid=response.user.id)
            for item in obj: # Can only be one, obj is only iterable
                occupationform = OccupationForm(initial={"student":item.student, "employer":item.employer})
        else:
            occupationform = OccupationForm()
        return render(response, "register/editprofile.html", {"form":form, "occupation":occupationform, "employer":CheckEmployer(response) })

        # "username":response.user.username, "email":response.user.email