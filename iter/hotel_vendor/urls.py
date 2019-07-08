from django.urls import path,include, re_path
from django.conf.urls import url
from . import views

app_name = 'hotel_vendor'

urlpatterns = [
    path('home', views.home, name="home"),
    path('add_hotel', views.add_hotel, name="add_hotel"),
    path('addroom/<int:pk>',views.add_room,name='add_room'),
    path('home/<int:pk>', views.hotel_detail, name="hotel_detail"),

]
