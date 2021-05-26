from django import forms  
from main.models import Locations, CareerType, TimePerWeek

class SearchJob(forms.Form):
    job = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class' : 'form-control mr-sm-2', 'placeholder': 'Search Job, Location...'}), required = False, label="")
    locations = forms.ModelChoiceField(queryset=Locations.objects.all().order_by('location'), required = False, label="", empty_label="Location")
    careertype = forms.ModelChoiceField(queryset=CareerType.objects.all().order_by('career'), required = False, label="", empty_label="Career")
    hours = forms.ModelChoiceField(queryset=TimePerWeek.objects.all().order_by('timeperweek'), required = False, label="", empty_label="Hours")

class AddJob(forms.Form):
    title = forms.CharField(max_length=200, label='Title', required = True)
    company = forms.CharField(max_length=200, label='Company', required = True)
    email = forms.CharField(max_length=200, label='Email', required = True)
    description = forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":20}))
    locations = forms.ModelChoiceField(queryset=Locations.objects.all().order_by('location'), label='Location', required = True)
    careertype = forms.ModelChoiceField(queryset=CareerType.objects.all().order_by('career'), label='Career Type', required = True)
    hours = forms.ModelChoiceField(queryset=TimePerWeek.objects.all().order_by('timeperweek'), label='Hours Per Week', required = True)


class EmployerApplication(forms.Form):
    company = forms.CharField(max_length=200, required = True, label="Company")
    email = forms.CharField(max_length=200, required = True, label="Email")
    ownershipproof = forms.FileField(label="Proof Of Ownership")


class StudentApplication(forms.Form):
    school = forms.CharField(max_length=200, required = True, label="School")
    email = forms.CharField(max_length=200, required = True, label="Email")
    studyproof = forms.FileField(label="Proof Of Study")