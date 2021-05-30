from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django import forms
from django.contrib.auth.models import User
from register.models import Themes

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]



class EditProfile(UserChangeForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email"]

class OccupationForm(forms.Form):
    employer = forms.BooleanField(required=False)
    student = forms.BooleanField(required=False)

class ThemeForm(forms.Form):
    theme = forms.ModelChoiceField(queryset=Themes.objects.filter(userid = "categories"),required = True, label="", empty_label="Theme")
