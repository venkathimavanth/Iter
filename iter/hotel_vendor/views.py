from django.shortcuts import render
from .forms import hotel_details,room_details
from hotel_booking.models import Hotels,Rooms
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def list_hotel(request):
    if request.method=='POST':

        form=hotel_details(request.POST,request.user)
        if form.is_valid():
            name=form.cleaned_data.get('name')
            address=form.cleaned_data.get('address')
            city=form.cleaned_data.get('city')
            state=form.cleaned_data.get('state')
            country=form.cleaned_data.get('country')
            email=form.cleaned_data.get('email')
            phone_number=form.cleaned_data.get('phone_number')
            data=Hotels.objects.create(name=name,address=address,city=city,state=state,country=country,phone_number=phone_number,email=email,user=request.user)
            data.save()
        return render(request,'hotel_vendor/home.html')
    else:
        form=hotel_details()
        return render(request,'hotel_vendor/hotel_details.html',{'form':form})

def add_room_type(request):
    if request.method=='POST':
        hotel=Hotels.objects.get(user=request.user)
        print(request.user)
        print(hotel.hotel_id)
        form=room_details(request.POST,request.user)
        if form.is_valid():
            x=form.cleaned_data
            print(x)
            room_type=form.cleaned_data.get('room_type')
            room_fac=form.cleaned_data.get('room_fac')
            cost=form.cleaned_data.get('cost')
            price=form.cleaned_data.get('price')
            availability=form.cleaned_data.get('availability')
            capacity=form.cleaned_data.get('capacity')

            data=Rooms.objects.create(room_type=room_type,room_fac=room_fac,cost=cost,price=price,availability=availability,capacity=capacity,hotel_id=hotel)
            data.save()
        return render(request,'hotel_vendor/home.html')
    else:
        form=room_details()
        return render(request,'hotel_vendor/room_details.html',{'form':form})
