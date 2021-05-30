
from django.contrib.auth.forms import UserChangeForm
from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from .forms import RegisterForm, EditProfile, OccupationForm, ThemeForm
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.models import User
from django.views import generic
from register.models import Occupation, Themes
from django.contrib.auth.forms import PasswordResetForm, PasswordChangeForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib import messages #import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Checks theme
def CheckDarkTheme(response):
    obj = Themes.objects.all()
    if (obj.filter(userid=response.user.id).exists()):
        obj = obj.filter(userid=response.user.id)
        for item in obj:
            if (item.theme == "dark"):
                return 'dark'
            else:
                return 'light'
    else:
        return 'light'

# Checks if employer
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
            messages.success(response, 'Accouny Successfully Created')
        return redirect("/login")
    else:
        form = RegisterForm()
        return render(response, "register/register.html", {"form": form, 'theme':CheckDarkTheme(response)})

@login_required
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
            obj = Occupation(
                userid=response.user.id, student=occupationform.cleaned_data["student"], employer=occupationform.cleaned_data["employer"])
            obj.save()

        obj = Themes.objects.all()
        if (obj.filter(userid=response.user.id).exists()):
            obj.filter(userid=response.user.id).delete()

        themeform = ThemeForm(response.POST)
        if themeform.is_valid():
            print(str(response.user.id))
            obj = Themes(theme=themeform.cleaned_data["theme"], userid=response.user.id)
            obj.save()
        messages.success(response, 'Settings Successfully Updated')
        return redirect("/")
    else:
        form = EditProfile(instance=response.user)
        obj = Occupation.objects.all()
        if (obj.filter(userid=response.user.id).exists()):
            obj = obj.filter(userid=response.user.id)
            for item in obj:  # Can only be one, obj is only iterable
                occupationform = OccupationForm(
                    initial={"student": item.student, "employer": item.employer})
        else:
            occupationform = OccupationForm()

        obj = Themes.objects.all()
        if (obj.filter(userid=response.user.id).exists()):
            obj = obj.filter(userid=response.user.id)
            for item in obj:  # Can only be one, obj is only iterable
                if (item.theme == 'dark'):
                    theme = 2
                else:
                    theme = 1
                themeform = ThemeForm(initial={"theme": theme})
        else:
            themeform = ThemeForm()
        return render(response, "register/editprofile.html", {"form": form, "occupation": occupationform, "employer": CheckEmployer(response), "themeform": themeform, 'theme':CheckDarkTheme(response)})

        # "username":response.user.username, "email":response.user.email


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "register/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com',
                                  [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
            messages.success(request, 'A message with reset password instructions has been sent to your inbox.')
            return redirect("/")
    password_reset_form = PasswordResetForm()
    return render(request, "register/password_reset.html", {"password_reset_form": password_reset_form, "theme":CheckDarkTheme(request)})

def passworddone(request):
    return redirect("/", {"theme":CheckDarkTheme(request)})

@login_required
def passwordchange(request):
    passwordchangeform = PasswordChangeForm()
    return render(request, "register/change-password.html",{"form":passwordchangeform, "theme":CheckDarkTheme(request)})
