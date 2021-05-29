from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('addjob/', views.addjob, name='addjob'),
    path('job/<int:id>', views.job, name='job'),
    path('about/', views.about, name='about'),
    path('studentreg/', views.studentreg, name='studentreg'),
    path('employerreg/', views.employerreg, name='employerreg'),
]