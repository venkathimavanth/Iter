from django.shortcuts import render
from .forms import hotel_search,Mycomments
from hotel_booking.models import Hotels,Rooms,Image,Comments,Hotel_Booking
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import random
import string
import math

def hotels(request):
    if request.method == "POST":
        print("hello...")
        form = hotel_search(request.POST)
        if form.is_valid():
            city_name = form.cleaned_data.get('city_name')
            From = form.cleaned_data.get('From')
            To = form.cleaned_data.get('To')
            hotels = Hotels.objects.filter(city=city_name)
            ratings = Comments.objects.values_list('rating',flat=True)
            sum = 0
            for rating in ratings:
                sum = sum + int(rating)
#            sum = round(sum/len(ratings),1)
            return render(request,'hotel_booking/hotels.html',{'form':form,'hotels' : hotels,'sum':sum})
        else:
            print(form.errors)
            form = hotel_search()
            return render(request,'hotel_booking/hotel_search.html',{'form':form})
    else:
        form = hotel_search()
        return render(request,'hotel_booking/hotel_search.html',{'form':form})

@login_required
def hotel(request,pk):
    user = request.user
    indi = False
    if pk:
        hotel = Hotels.objects.get(hotel_id=pk)
        rooms = Rooms.objects.filter(hotel_id=pk)
        images = hotel.all_images()
        comments = Comments.objects.filter(hotel_id=pk)
        if(Hotel_Booking.objects.filter(user=user).filter(hotel_id=pk)):
            indi = True
        if request.method == "POST":
            cform = Mycomments(request.POST)
            if cform.is_valid():
                comment = request.POST['comment']
                rating = cform.cleaned_data.get('rating')
                cmnt = Comments(user=user,hotel=hotel,comment=comment,rating=rating)
                cmnt.save()
        return render(request,'hotel_booking/hotel_detail.html',{'hotel':hotel,'rooms':rooms,'images':images,'comments':comments,'user':user,'indi':indi})
