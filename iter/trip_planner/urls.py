from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [

    path('planer/',views.trip_plan,name='trip_plan'),

    ]
