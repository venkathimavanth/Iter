from django.urls import path,include, re_path
from django.conf.urls import url
from . import views

app_name = 'hotel_booking'

urlpatterns = [
    path('hotels/',views.hotels,name="hotels"),
    path('hotels/<int:pk>', views.hotel,name="hotel"),
    path('hotels/booking/<int:pk>', views.Book,name="Book"),
    path('hotels/myhotelbookings', views.myhotelbookings,name="myhotelbookings"),    
]
