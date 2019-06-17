from django.shortcuts import render
from .forms import agency_details,bus_details
from bus_booking.models import Bus_agency,Bus
from django.contrib.auth.models import User
from user_authentication.models import Profile
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def list_agency(request):
    if request.method=='POST':

        form=agency_details(request.POST,request.user)
        if form.is_valid():
            name=form.cleaned_data.get('name')
            address=form.cleaned_data.get('address')
            email=form.cleaned_data.get('email')
            phone_number=form.cleaned_data.get('phone_number')
            data=Bus_agency.objects.create(name=name,address=address,phone_number=phone_number,email=email,user=request.user)
            data.save()
        return render(request,'bus_vendor/home.html')
    else:
        form=agency_details()
        return render(request,'bus_vendor/agency_details.html',{'form':form})

def add_bus(request):
    if request.method=='POST':
        agency=Bus_agency.objects.get(user=request.user)
        print(request.user)
        print(agency.agent_id)
        form=bus_details(request.POST,request.user)
        if form.is_valid():
            bus_type=form.cleaned_data.get('bus_type')
            bus_model=form.cleaned_data.get('bus_model')
            costperkm=form.cleaned_data.get('costperkm')
            serviceno=form.cleaned_data.get('serviceno')
            noseats=form.cleaned_data.get('noseats')
            start_city=form.cleaned_data.get('start_city')
            destination_city=form.cleaned_data.get('destination_city')

            data=Bus.objects.create(Bus_type=bus_type,Bus_model=bus_model,costperkm=costperkm,serviceno=serviceno,noseats=noseats,start_city=start_city,destination_city=destination_city,agency=agency)
            data.save()
        return render(request,'bus_vendor/home.html')
    else:
        form=bus_details()
        return render(request,'bus_vendor/bus_details.html',{'form':form})
