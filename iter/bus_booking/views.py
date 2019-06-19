from django.shortcuts import render
from .forms import passenger_details
from bus_booking.models import passenger,Bus_Booking
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
        return render(request,'bus_vendor/home.html')
    else:
        form=passenger_details()
        return render(request,'bus_vendor/agency_details.html',{'form':form})
