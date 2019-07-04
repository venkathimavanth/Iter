from django.shortcuts import render
from .forms import agency_details,bus_details,via_details,date_test,dateform
from bus_booking.models import Bus_agency,Bus,via,Bus_Booking,passenger
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
            noseats=40
            start_city=form.cleaned_data.get('start_city')
            destination_city=form.cleaned_data.get('destination_city')
            start=form.cleaned_data.get('start')
            reach=form.cleaned_data.get('reach')
            date=start.date()
            data=Bus.objects.create(Bus_type=bus_type,Bus_model=bus_model,costperkm=costperkm,serviceno=serviceno,noseats=noseats,start=start,reach=reach,date=date,start_city=start_city,destination_city=destination_city,agency=agency)
            data.save()
        return render(request,'bus_vendor/home.html')
    else:
        form=bus_details()
        print(form)
        return render(request,'bus_vendor/bus_details.html',{'form':form})

def add_via(request,pk):
    if request.method=='POST':

        print(request.user)

        form=via_details(request.POST,request.user)
        if form.is_valid():
            bus=Bus.objects.get(serviceno=form.cleaned_data.get('serviceno'))
            place_name=form.cleaned_data.get('place_name')
            reach=form.cleaned_data.get('reach')
            distance=form.cleaned_data.get('distance_from_startcity')

            data=via.objects.create(place_name=place_name,reach=reach,distance_from_startcity=distance,bus=bus)
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

        return render(request,'bus_vendor/home.html')
    else:
        form=via_details()
        return render(request,'bus_vendor/via.html',{'form':form,'pk':pk})

def current_buses(request):
    a=Bus_agency.objects.get(user=request.user)
    bus=Bus.objects.filter(agency=a)
    buses=[]
    for b in bus:
        vias=via.objects.filter(bus=b)
        buses.append([b,vias])

    return render(request,'bus_vendor/home.html',{'buses':buses})

def passengerlist(request,pk):
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
    elif pk:
        form=dateform()
        return render(request,'bus_vendor/passengerlist.html',{'form':form})

def date_testing(request):
    if request.method=="POST":
        form=date_test(request.POST)
        if form.is_valid():
            print(form.cleaned_data)


    else:
        form=date_test()
        return render(request,'bus_vendor/bus_dates.html',{'form':form})

def edit_agency(request):
    if request.method == 'POST':
        agency=Bus_agency.objects.get(user=request.user)
        form = agency_details(request.POST,instance=agency)
        if form.is_valid() :
            form.save()

            messages.success(request, ('Your profile was successfully updated!'))
            return redirect('user_authentication:edit_agency')
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        print('outside')
        agencys=Bus_agency.objects.get(user=request.user)
        print(agencys)
        form = agency_details(instance=agencys)

    return render(request, 'bus_vendor/edit_agency.html', {
            'form': form,        })
