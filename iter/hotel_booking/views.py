from django.shortcuts import render
from .forms import hotel_search,Mycomments,Book
from hotel_booking.models import Hotels,Rooms,Image,Comments,Hotel_Booking
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import random
import string
import uuid

def generate_uniq_ID():
    uniq_id = uuid.uuid4()
    return str(uniq_id)

def hotels(request):
    if request.method == "POST":
        print("hello...")
        form = hotel_search(request.POST)
        if form.is_valid():
            city_name = form.cleaned_data.get('city_name')
            From = form.cleaned_data.get('From')
            To = form.cleaned_data.get('To')
            hotels = Hotels.objects.filter(city=city_name)
            return render(request,'hotel_booking/hotels.html',{'form':form,'hotels' : hotels})
        else:
            print(form.errors)
            form = hotel_search()
            return render(request,'hotel_booking/hotel_search.html',{'form':form})
    else:
        form = hotel_search()
        return render(request,'hotel_booking/hotel_search.html',{'form':form})

def hotel(request,pk):
    user = request.user
    indi = False
    if pk:
        hotel = Hotels.objects.get(hotel_id=pk)
        rooms = Rooms.objects.filter(hotel_id=pk)
        images = hotel.all_images()
        comments = Comments.objects.filter(hotel_id=pk)
        print(Hotel_Booking.objects.filter(user=user).filter(hotel_id=pk))
        if(Hotel_Booking.objects.filter(user=user).filter(hotel_id=pk).count()):
            indi = True
        ratings = Comments.objects.filter(hotel=hotel).values_list('rating',flat=True)
        sum = 0
        tot_len = len(ratings)
        for rating in ratings:
            sum += rating
        if tot_len == 0:
            sum = 3.5
        else:
            sum = round(sum/tot_len,1)
        sum=int(sum*10)
        if request.method == "POST":
            cform = Mycomments(request.POST)
            if cform.is_valid():
                comment = cform.cleaned_data.get('comment')
#                if 'rating' in request.POST:
#                    print(indi)
#                    print(request.POST.get('rating'))
#                else:
#                    print(False)
                rating = int(request.POST.get('rating'))
                print("Rating:" + str(rating) + " Type:" + str(type(rating)))
                print(rating)
                cmnt = Comments(user=user,hotel=hotel,comment=comment,rating=rating)
                cmnt.save()
        else:
            cform = Mycomments()
        return render(request,'hotel_booking/hotel_detail.html',{'sum':sum,'cform':cform,'hotel':hotel,'rooms':rooms,'images':images,'comments':comments,'user':user,'indi':indi})

@login_required(login_url='user_authentication:user_login')
def Book(request,pk):
    if pk:
        user = request.user
        if request.method == "POST":
            fname = request.POST['fname']
            lname = request.POST['lname']
            gender = request.POST['gender']
            age = request.POST['age']
            Arr_date = request.POST['Arr_date']
            Stime = request.POST['Stime']
            Dep_date = request.POST['Dep_date']
            Etime = request.POST['Etime']
            room_type = request.POST['room_type']
            room_fac = request.POST['room_fac']
            name = str(fname) + " " + str(lname)
            hotel = Hotels.objects.get(hotel_id=pk)
            uni_id = generate_uniq_ID()
            print(uni_id)
            room = Rooms.objects.filter(hotel_id=pk).filter(room_type=room_type).filter(room_fac=room_fac)
            # print("--------------------------------------------")
            # print(room)
            # print("--------------------------------------------")
            for r in room:
                avail = r.availability
                id = r.id
            if avail == 0:
                return render(request,'hotel_booking/sorry.html',{'hotel':hotel,'r':r})
            else:
                room_new = Rooms.objects.get(id=id)
                room_new.availability -= 1
                print(room_new.availability)
                room_new.save()
            booking = Hotel_Booking(user=user,name=name,gender=gender,age=age,room_type=room_type,room_fac=room_fac,fromdate=Arr_date,fromtime=Stime,todate=Dep_date,totime=Etime,hotel=hotel,booking_id=uni_id)
            booking.save()
            return render(request,'hotel_booking/timer.html',{'hotel':hotel,'r':r})
        else:
            return render(request,'hotel_booking/booking.html')

def myhotelbookings(request):
    booking=Hotel_Booking.objects.filter(user=request.user)
    return render(request,'hotel_booking/myhotelbooking.html',{'book_info':booking})
