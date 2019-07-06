from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [

    path('planer-city=/(?P<value>\d+)/',views.trip_city,name='trip_city'),
    path('planer/',views.trip_plan,name='trip_plan'),
    path('home/',views.trip_home,name='trip_home'),

    ]
