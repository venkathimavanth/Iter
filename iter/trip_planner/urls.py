from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [

    path('planer/',views.trip_plan,name='trip_plan'),
    path('home/',views.trip_home,name='trip_home'),
    path('my_plans/',views.my_plans,name='my_plans'),
    path('saveplan=/(?P<value>\d+)/',views.save_my_plan,name='save_my_plan'),

    ]
