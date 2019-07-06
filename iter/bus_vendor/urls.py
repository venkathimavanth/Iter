from django.urls import path,include, re_path
from django.conf.urls import url
from . import views

app_name = 'bus_vendor'

urlpatterns = [
    path('', views.list_agency,name="list_agency"),
    path('add_bus/', views.add_bus,name="add_bus"),
    path('add_via/<int:pk>', views.add_via,name="via"),
    path('date_test/<int:pk>',views.date_testing,name="date_testing"),
    path('buses/',views.current_buses,name="current_buses"),
    path('passengerlist/<int:pk>',views.passengerlist,name="passengerlist"),
    path('edit_agency',views.edit_agency,name="edit_agency"),



]
