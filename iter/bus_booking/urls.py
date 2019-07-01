from django.urls import path,include, re_path
from django.conf.urls import url
from . import views

app_name = 'bus_booking'

urlpatterns = [
    path('buses',views.buses,name="buses"),
    path('buses/<int:pk>', views.bus_detail,name="bus_detail"),
    path('test', views.test,name="test"),


]
