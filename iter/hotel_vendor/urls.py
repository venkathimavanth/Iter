from django.urls import path,include, re_path
from django.conf.urls import url
from . import views

app_name = 'hotel_vendor'

urlpatterns = [
    path('', views.list_hotel, name="list_hotel"),
    path('add_room_type/',views.add_room_type,name='add_room_type'),


]
