
from django.urls import path,include, re_path
from django.conf.urls import url
from . import views

app_name = 'user_authentication'

urlpatterns = [
    path('', views.user_login, name="user_login"),
    path('logout/',views.logoutuser, name="logout"),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate,
        name='activate'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('password/', views.change_password, name='change_password'),
    path('signup/',views.signup,name='signup'),
    path('bussignup/',views.bussignup,name='bussignup'),
    path('hotelsignup/',views.hotelsignup,name='hotelsignup'),


]
