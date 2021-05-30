
from django.shortcuts import render, redirect
from .forms import SearchJob, AddJob, EmployerApplication, StudentApplication
from main.models import Locations, CareerType, TimePerWeek, Jobs
from register.models import Occupation
from django.contrib import messages #import messages
from register.models import Themes

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
#Checks if student
def CheckStudent(response):
    obj = Occupation.objects.all()
    if (obj.filter(userid=response.user.id).exists()): 
        obj = obj.filter(userid=response.user.id)
        for item in obj:
            if (item.student == True):
                return True
            else:
                return False
    else:
        return False


def home(response):
    # Populate search filters with database items
    locations = Locations.objects.all().order_by('location')
    careertype = CareerType.objects.all().order_by('career')
    hours = TimePerWeek.objects.all().order_by('timeperweek')
    if response.method == "POST":
        Mainform = SearchJob(response.POST, initial={"locations":locations, "careers":careertype, "hours":hours})
        if Mainform.is_valid():
            #Filter Job Database
            jobobjects = Jobs.objects.all()
            if (Mainform.cleaned_data["locations"] != None):
                jobobjects = jobobjects.filter(location=Mainform.cleaned_data["locations"])

            if (Mainform.cleaned_data["hours"] != None):
                jobobjects = jobobjects.filter(hours=Mainform.cleaned_data["hours"])
                
            if (Mainform.cleaned_data["careertype"] != None):
                jobobjects = jobobjects.filter(careertype=Mainform.cleaned_data["careertype"])
            return render(response, "main/jobs.html", {"MainSearchForm":Mainform, "jobs":jobobjects, "employer":CheckEmployer(response), "theme":CheckDarkTheme(response)})
    else:
        Mainform = SearchJob(initial={"locations":locations, "careers":careertype, "hours":hours})
        n = " "
        return render(response, "main/home.html", {"MainSearchForm":Mainform, "employer":CheckEmployer(response), "theme":CheckDarkTheme(response)})

def addjob(response):
    if response.method == "POST":
        addjobform = AddJob(response.POST)
        if addjobform.is_valid():
            # Get Form Choices
            q = Jobs(
                title=addjobform.cleaned_data["title"],
                company=addjobform.cleaned_data["company"],
                description=addjobform.cleaned_data["description"],
                careertype=addjobform.cleaned_data["careertype"],
                location=addjobform.cleaned_data["locations"],
                hours=addjobform.cleaned_data["hours"]
                )
            q.save()
            messages.success(response, 'A job has successfully been added')
            return redirect('/')
        else:  
            print('Adding Job Failed')
            addjobform = AddJob()
            return render(response, "main/addjob.html", {"addjobform":addjobform, "employer":CheckEmployer(response), "theme":CheckDarkTheme(response)})
    else:
        addjobform = AddJob()
        return render(response, "main/addjob.html", {"addjobform":addjobform, "employer":CheckEmployer(response), "theme":CheckDarkTheme(response)})


def job(response, id):
    obj = Jobs.objects.all()
    jobobjects = obj.filter(id=id)  
    return render(response, "main/job.html", {"job":jobobjects, "employer":CheckEmployer(response), "student":CheckStudent(response), "theme":CheckDarkTheme(response)})


def about(response):
    return render(response, "main/about.html", {"employer":CheckEmployer(response), "theme":CheckDarkTheme(response)})


def studentreg(response):
    if response.method == "POST":
        messages.success(response, 'A application has successfully been submitted')
        return redirect("/home")
    else:
        form = StudentApplication()
        return render(response, "main/applystudent.html", {"employer":CheckEmployer(response), "form":form, "theme":CheckDarkTheme(response)})


def employerreg(response):
    if response.method == "POST":
        messages.success(response, 'A application has successfully been submitted')
        return redirect("/home")
    else:
        form = EmployerApplication()
        return render(response, "main/applyemployer.html", {"employer":CheckEmployer(response), "form":form, "theme":CheckDarkTheme(response)})

