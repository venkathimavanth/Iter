from django.urls import path,include, re_path
from django.conf.urls import url
from . import views

app_name = 'bus_vendor'

urlpatterns = [
    path('', views.list_agency,name="list_agency"),
    path('add_bus/', views.add_bus,name="add_bus"),
    path('add_via/', views.add_via,name="via")


]
