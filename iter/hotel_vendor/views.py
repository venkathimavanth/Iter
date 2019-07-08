from django.shortcuts import render
from hotel_booking.models import Hotels,Rooms,Comments,Image,Hotel_Booking
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory

@login_required
def add_hotel(request):

    if request.method=='POST':
        # ImageFormset = modelformset_factory(Image,fields=("image",))
        # formset = ImageFormset(request.POST, request.FILES)
#        images = request.FILES.getlist('image')
        name=request.POST.get('hname')
        address=request.POST.get('address')
        city=request.POST.get('city')
        state=request.POST.get('state')
        country=request.POST.get('country')
        email=request.POST.get('email')
        phone_number=request.POST.get('phone_number')
        desc=request.POST.get('description')
        lat=request.POST.get('lat')
        long=request.POST.get('long')
        hotel=Hotels(user=request.user,name=name,address=address,city=city,state=state,country=country,phone_number=phone_number,email=email,description=desc,lat=lat,long=long)
        new_hotel=hotel.save()
        # print(formset)
        ho=Hotels.objects.get(user=request.user)
#        print(request.POST)
        print("-----------------------------------------------------")
        print(request.FILES)
        print("-----------------------------------------------------")
        for file in request.FILES.getlist('images'):
            print(file)
            i=Image(image=file,hotel=ho)
            i.save()

        # if formset.is_valid():
        #     print("hello")
        #     for f in formset:
        #         print(f.cleaned_data)
        #         i1=f.cleaned_data.get('image')
        #         print(i1)
        #         i=Image.objects.create(hotel=Hotels.objects.get(user=request.user),image=i1)
        #
        #         i.save()

        return render(request,'hotel_vendor/re-directing.html',{'hotel':hotel})
    else:
        # ImageFormset = modelformset_factory(Image,fields=("image",), extra=4)
        # formset = ImageFormset()
        return render(request,'hotel_vendor/add_hotel_form.html')

@login_required
def add_room(request,pk):
    if pk:
        if request.method=='POST':
            hotel=Hotels.objects.get(hotel_id=pk)
            print(request.user)
            print(hotel.hotel_id)
            room_type=request.POST.get('room_type')
            room_fac=request.POST.get('room_fac')
            cost=request.POST.get('cost')
            price=request.POST.get('price')
            availability=request.POST.get('avail')
            capacity=request.POST.get('num_per')
            room1 = Rooms.objects.filter(hotel_id=pk).filter(room_type=room_type).filter(room_fac=room_fac).count()
            if room1==0:
                r=Rooms.objects.create(hotel_id=hotel,room_type=room_type,room_fac=room_fac,price=price,cost=cost,availability=availability,capacity=capacity)
                r.save()

                return render(request,'hotel_vendor/re-directing.html',{'r':r})
            else:
                room = Rooms.objects.filter(hotel_id=pk).filter(room_type=room_type).filter(room_fac=room_fac)
                for r in room:
                    avail = r.availability
                    id = r.id
                room_new=Rooms.objects.get(id=id)
                room_new.availability += avail
#            print(room_new.availability)
                room_new.save()

#            room=Rooms(hotel_id=hotel,room_type=room_type,room_fac=room_fac,cost=cost,price=price,availability=availability,capacity=capacity)
#            room.save()
                return render(request,'hotel_vendor/re-directing.html',{'room':room})
        else:
            return render(request,'hotel_vendor/add_room_form.html')

@login_required
def home(request):
    hotels = Hotels.objects.filter(user=request.user)
    return render(request,'hotel_vendor/home.html',{'hotels':hotels})

@login_required
def hotel_detail(request,pk):
    user = request.user
    indi = False
    if pk:
        hotel = Hotels.objects.get(hotel_id=pk)
        rooms = Rooms.objects.filter(hotel_id=pk)
        images = hotel.all_images()
        ratings = Comments.objects.filter(hotel=hotel).values_list('rating',flat=True)
        book_info = Hotel_Booking.objects.filter(hotel=hotel)
        sum = 0
        tot_len = len(ratings)
        for rating in ratings:
            sum += rating
        if tot_len == 0:
            sum = 3.5
        else:
            sum = round(sum/tot_len,1)
        return render(request,'hotel_vendor/hotel_details.html',{'book_info':book_info,'rooms':rooms,'sum':sum,'hotel':hotel,'rooms':rooms,'images':images,'user':user})
