from django.shortcuts import render
from .forms import passenger_details,bus_search
from bus_booking.models import passenger,Bus_Booking,Bus
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import random
import string

def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def gen_booking_id(request):
    order_new_id= random_string_generator()

    qs_exists= Bus_Booking.objects.filter(booking_id= order_new_id).exists()
    if qs_exists:
        return unique_order_id_generator()
    return order_new_id




@login_required
def passenger_details(request):
    if request.method=='POST':
        booking_id=gen_booking_id()
        form=passenger_details(request.POST,request.user)
        if form.is_valid():
            name=form.cleaned_data.get('name')
            gender=form.cleaned_data.get('gender')
            age=form.cleaned_data.get('age')
            seatno=1
            data=passenger.objects.create(name=name,gender=gender,age=age,seatno=seatno,booking_id=booking_id)
            data.save()
        return render(request,'bus_booking/home.html')
    else:
        form=passenger_details()
        return render(request,'bus_booking/passenger_details.html',{'form':form})

def buses(request):
    if request.method=='POST':
        print("posted")
        form = bus_search(request.POST,request.user)
        if form.is_valid():
            start_city=form.cleaned_data.get('start_city')
            destination_city=form.cleaned_data.get('destination_city')
            start_date=form.cleaned_data.get('start_date')
            buses=Bus.objects.filter(start_date=start_date)
            bus_list=[]
            for x in buses:
                if x.destination_city==destination_city and x.start_city==start_city:
                    bus_list.append(x)

                elif x.via:
                    y=via.objects.filter(bus=x)
                    for z in y:
                        for a in y:
                            if z.place_name==start_city and a.place_name==destination_city:
                                bus_list.append(x)

                    for z in y:

                        if (x.start_city==start_city and z.place_name==destination_city) or (x.destination_city==destination_city and z.place_name==start_city):
                            bus_list.append(x)
            return render(request,'bus_booking/buses.html',{'form':bus_list})


        else:
            print('form1')
            form = bus_search()
            return render(request,'bus_booking/search.html',{'form':form})
    else:
        print('form')
        form = bus_search()
        return render(request,'bus_booking/search.html',{'form':form})

def test(request):
    return render(request,'bus_booking/try3.html')



def bus_detail(request,primary_key):
    if primary_key:
        bus=Bus.object.get(serviceno=primary_key)
        return render(request,'bus_booking/bus_detail.html',{'bus':bus})
