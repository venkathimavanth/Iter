from django.shortcuts import render,redirect
from .forms import agency_details,bus_details,via_details,date_test,dateform,service
from bus_booking.models import Bus_agency,Bus,via,Bus_Booking,passenger,bus_dates
from django.contrib.auth.models import User
from user_authentication.models import Profile
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect
from datetime import datetime,timedelta
from django.urls import reverse
# Create your views here.
@login_required
def list_agency(request):
    if request.user.profile.user_type=='B':
        if request.method=='POST':
            form=agency_details(request.POST,request.user)
            if form.is_valid():
                name=form.cleaned_data.get('name')
                address=form.cleaned_data.get('address')
                email=form.cleaned_data.get('email')
                phone_number=form.cleaned_data.get('phone_number')
                data=Bus_agency.objects.create(name=name,address=address,phone_number=phone_number,email=email,user=request.user)
                data.save()
                return redirect('bus_vendor:current_buses')
            else:
                form=agency_details()
                return render(request,'bus_vendor/agency_details.html',{'form':form})
        else:
            form=agency_details()
            return render(request,'bus_vendor/agency_details.html',{'form':form})
    else:
        return HttpResponse("Page not Found")

def add_bus(request):
    if request.user.profile.user_type=='B':
        if request.method=='POST':
            agency=Bus_agency.objects.get(user=request.user)
            print(request.user)
            print(agency.agent_id)
            form=bus_details(request.POST,request.user)
            print(form.errors)
            if form.is_valid():
                bus_type=form.cleaned_data.get('bus_type')
                bus_model=form.cleaned_data.get('bus_model')
                costperkm=form.cleaned_data.get('costperkm')
                serviceno=form.cleaned_data.get('serviceno')
                noseats=40
                start_city=form.cleaned_data.get('start_city')
                destination_city=form.cleaned_data.get('destination_city')
                start=form.cleaned_data.get('start')
                reach=form.cleaned_data.get('reach')
                date=start.date()
                journeytime=form.cleaned_data.get('journeytime')
                data=Bus.objects.create(Bus_type=bus_type,Bus_model=bus_model,costperkm=costperkm,journeytime=journeytime,serviceno=serviceno,noseats=noseats,start=start,reach=reach,date=date,start_city=start_city,destination_city=destination_city,agency=agency)
                data.save()
                return redirect( 'bus_vendor:date_testing' ,pk=serviceno )
            else:
                form=bus_details()
                print(form)
                return render(request,'bus_vendor/bus_details.html',{'form':form})
        else:
            form=bus_details()
            print(form)
            return render(request,'bus_vendor/bus_details.html',{'form':form})
    else:
        return HttpResponse("Page not Found")

def add_via(request,pk):
    if request.user.profile.user_type=='B':
        if request.method=='POST':

            print(request.user)

            form=via_details(request.POST,request.user)
            print(form.errors)
            if form.is_valid():
                bus=Bus.objects.get(serviceno=form.cleaned_data.get('serviceno'))
                place_name=form.cleaned_data.get('place_name')
                reach=form.cleaned_data.get('reach')
                distance=form.cleaned_data.get('distance_from_startcity')
                journeytime=form.cleaned_data.get('journeytime')

                data=via.objects.create(place_name=place_name,reach=reach,distance_from_startcity=distance,journeytime=journeytime,bus=bus)
                data.save()

                bus=Bus.objects.get(serviceno=form.cleaned_data.get('serviceno'))
                n=bus.noseats
                via1=via.objects.filter(bus=form.cleaned_data.get('serviceno'))
                print(via1)
                j=2
                for i in via1:
                    j=j+1
                k=''
                l = 0
                for l in range(n):
                    k=k+'.'*j +','
                print(k)
                bus.seats_available=k
                bus.save()

                return redirect(reverse('bus_vendor:current_buses'))
            else:
                print(form.errors)
                form=via_details()
                return render(request,'bus_vendor/via.html',{'form':form,'pk':pk})
        else:
            form=via_details()
            return render(request,'bus_vendor/via.html',{'form':form,'pk':pk})
    else:
        return HttpResponse("Page not Found")

def current_buses(request):
    if request.user.profile.user_type=='B':
        a=Bus_agency.objects.get(user=request.user)
        bus=Bus.objects.filter(agency=a)
        buses=[]

        for b in bus:
            vias=via.objects.filter(bus=b)
            dates=bus_dates.objects.filter(bus=b)
            buses.append([b,vias,dates])

        return render(request,'bus_vendor/home.html',{'buses':buses})
    else:
        return HttpResponse("Page not Found")

def passengerlist(request,pk):
    if request.user.profile.user_type=='B':
        if request.method=="POST":
            form=dateform(request.POST)
            if form.is_valid():
                date=form.cleaned_data['date']
                total=[]
                bookings=Bus_Booking.objects.filter(bus_start_date=date,serviceno=pk)
                for b in bookings:
                    passengers=passenger.objects.filter(booking_id=b)
                    for p in passengers:
                        total.append([p.name,p.seatno,p.booking_id.booking_id,b.start_city,b.destination_city])
                return render(request,'bus_vendor/passengerlist.html',{'form':form,'total':total})
            else:
                form=dateform()
                return render(request,'bus_vendor/passengerlist.html',{'form':form})
        elif pk:
            form=dateform()
            return render(request,'bus_vendor/passengerlist.html',{'form':form})
    else:
        return HttpResponse("Page not Found")

def date_testing(request,pk):
    if request.user.profile.user_type=='B':
        if request.method=="POST":
            form=date_test(request.POST)
            print('true1')
            print(form.errors)
            if form.is_valid():
                print('true2')
                serviceno=pk
                fromdate=form.cleaned_data['fromdate']
                mon=form.cleaned_data['monday']
                tue=form.cleaned_data['tuesday']
                wed=form.cleaned_data['wednesday']
                thu=form.cleaned_data['thursday']
                fri=form.cleaned_data['friday']
                sat=form.cleaned_data['saturday']
                sun=form.cleaned_data['sunday']
                tilldate=form.cleaned_data['tilldate']
                days=[]

                if mon:
                    days.append(0)
                if tue:
                    days.append(1)
                if wed:
                    days.append(2)
                if thu:
                    days.append(3)
                if fri:
                    days.append(4)
                if sat:
                    days.append(5)
                if sun:
                    days.append(6)

                dates=[]
                print(days)
                delta = tilldate - fromdate
                for i in range(delta.days + 1):
                    if (fromdate + timedelta(days=i)).weekday() in days:
                        dates.append(fromdate + timedelta(days=i))
                print(dates)
                bus=Bus.objects.get(serviceno=serviceno)
                dates_query_exist=bus_dates.objects.filter(bus=bus)
                dates_exist=[]
                for d in dates_query_exist:
                    dates_exist.append(str(d.date.date()))
                print(dates_exist)
                for d in dates :
                    print(str(d.date()))
                    if str(d.date()) not in dates_exist:
                        print('hii')
                        dd=bus_dates.objects.create(bus=bus,date=d)
                        dd.save()
                return redirect('bus_vendor:current_buses')
            else:
                form=date_test()
                print(form)
                return render(request,'bus_vendor/bus_dates.html',{'form':form})
        else:
            form=date_test()
            print(form)
            return render(request,'bus_vendor/bus_dates.html',{'form':form})
    else:
        return HttpResponse("Page not Found")



def edit_agency(request):
    if request.user.profile.user_type=='B':
        if request.method == 'POST':
            agency=Bus_agency.objects.get(user=request.user)
            form = agency_details(request.POST,instance=agency)
            if form.is_valid() :
                print(form)
                form.save()

                return redirect('bus_vendor:edit_agency')
            else:
                print(form.errors)
        else:
            print('outside')
            agencys=Bus_agency.objects.get(user=request.user)
            print(agencys)
            form = agency_details(instance=agencys)

            return render(request, 'bus_vendor/edit_agency.html', {
            'form': form,        })
    else:
        return HttpResponse("Page not Found")
