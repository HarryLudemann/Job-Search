from django.db import models

# Create your models here.
class Jobs(models.Model):
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    careertype = models.CharField( max_length=100)
    hours = models.CharField(max_length=20)
    location = models.CharField(max_length=100)
    email = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title
        return self.company
        return self.careertype
        return self.hours
        return self.description
        return self.date
        return self.enddate
    

class Locations(models.Model):
    location = models.CharField(max_length=200)
    def __str__(self):
        return self.location

class CareerType(models.Model):
    career = models.CharField(max_length=200)
    def __str__(self):
        return self.career

class TimePerWeek(models.Model):
    timeperweek = models.CharField(max_length=200)
    def __str__(self):
        return self.timeperweek
