from django.contrib import admin
from main.models import Jobs, Locations, CareerType, TimePerWeek

# Register your models here.
admin.site.register(Jobs)
admin.site.register(Locations)
admin.site.register(CareerType)
admin.site.register(TimePerWeek)