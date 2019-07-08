from django.urls import path,include, re_path
from django.conf.urls import url
from . import views

app_name = 'bus_booking'

urlpatterns = [
    path('',views.buses,name="buses"),
    path('buses/<int:pk>', views.bus_detail,name="bus_detail"),
    path('test', views.test,name="test"),
    path('passengerdetails',views.passengerdetails,name="passengerdetails"),
    path('mybookings',views.mybookings,name="mybookings"),
    path('busticket',views.busticket,name="busticket")
#    path('mybookings/<int:pk>', views.bookingdetail,name="bookingdetail"),
#    url(r'^mybookings/(?P<slug>[-\w]+)/$', views.bookingdetail, name='bookingdetail'),


]
