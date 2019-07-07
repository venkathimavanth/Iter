from django.shortcuts import render,redirect
from .forms import passenger_details,bus_search,contactform
from bus_booking.models import passenger,Bus_Booking,Bus,via,bus_dates
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import random
import string
import json
from django.forms import formset_factory
from datetime import datetime,timedelta
from django.core.mail import EmailMessage, send_mail

def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def gen_booking_id(request):
    order_new_id= random_string_generator()

    qs_exists= Bus_Booking.objects.filter(booking_id= order_new_id).exists()
    if qs_exists:
        return unique_order_id_generator()
    return order_new_id




#@login_required(login_url='user_authentication:user_login')
def passengerdetails(request):
    print('true')
    if request.method=='POST':
        print('false')
        booking_id=gen_booking_id(request)
        print(booking_id)
        bus=Bus.objects.get(serviceno=request.session['pk'])
        v=via.objects.filter(bus=bus)
        dates=bus_dates.objects.filter(bus=bus)
        if bus.start_city==request.session['start_city']:
            print('here')
            distance1=0
            for d in dates:
                print(d.date.date())

                print(request.session['start_date'])
                if str(d.date.date())==request.session['start_date']:
                    b_s_d=d.date.date()
                    start=d.date
                    print('here1')
                    j=bus.journeytime
        for a in v:
            if a.place_name.lower()==request.session['start_city'].lower():
                distance1=0
                for d in dates:
                    if (d.date + timedelta(minutes=a.journeytime)).date()==request.session['start_date']:
                        b_s_d=d.date.date()
                        start=d.date + timedelta(minutes=a.journeytime)
                        j=a.journeytime
            if a.place_name.lower()==request.session['destination_city'].lower():
                distance2=a.distance_from_startcity
                reach=start + timedelta(minutes=(a.journeytime - j))

        if bus.destination_city==request.session['destination_city']:
            distance2=bus.distance_from_startcity
            reach=start + timedelta(minutes=j)
        conform=contactform(request.POST)
        s=request.session['seats_selected']
        fare=(distance2 - distance1)*bus.costperkm * len(s)

        if conform.is_valid():
            phone_number=conform.cleaned_data.get('phone_number')
            email=conform.cleaned_data.get('email')
            if request.user.is_authenticated:

                data1=Bus_Booking.objects.create(bus_type=bus.Bus_type,fare=fare,Bus_model=bus.Bus_model,start_city=request.session['start_city'],destination_city=request.session['destination_city'],bus_start_date=b_s_d,start=start,reach=reach,serviceno=bus,booking_id=booking_id,phone_number=phone_number,email=email,user=request.user)
                data1.save()
            else:
                data1=Bus_Booking.objects.create(bus_type=bus.Bus_type,fare=fare,Bus_model=bus.Bus_model,start_city=request.session['start_city'],destination_city=request.session['destination_city'],bus_start_date=b_s_d,start=start,reach=reach,serviceno=bus,booking_id=booking_id,phone_number=phone_number,email=email)
                data1.save()

        formi=formset_factory(passenger_details)
        forma=formi(request.POST)
        print(request.POST)
        s=request.session['seats_selected']
        n=-1
        messages=''
        if forma.is_valid():
            print('true')
            for f in forma:
                print(f)
                n=n+1
                name=f.cleaned_data.get('name')
                gender=f.cleaned_data.get('gender')
                age=f.cleaned_data.get('age')
                seatno=s[n]
                bok=Bus_Booking.objects.get(booking_id=booking_id)
                data=passenger.objects.create(name=name,gender=gender,age=age,seatno=seatno,booking_id=bok)
                data.save()
                messages=messages+'Passenger Name  :'+str(name)+"\n"+'Gender  :'+str(gender)+"\n"+'Age  :'+str(age)+"\n"+'Seat No  :'+str(seatno)+'\n'
            mail_subject = 'Activate your Iter account.'
            message = str(messages)
            to_email = conform.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()


            book=Bus_Booking.objects.get(booking_id=booking_id)
            passe=passenger.objects.filter(booking_id=book)
            print(forma.errors)
            return render(request,'bus_booking/busticket.html',{'book':book,'passe':passe})
    else:
        j=request.session['noss']
        form = formset_factory(passenger_details, extra=j-1, min_num=1)
        print('true')
        conform=contactform()
        return render(request,'bus_booking/passenger_details.html',{'form':form,'contactaform':conform})

def buses(request):

    if request.method=='POST':
        print("posted")
        form = bus_search(request.POST)

        if form.is_valid():
            start_city=form.cleaned_data.get('start_city')
            destination_city=form.cleaned_data.get('destination_city')
            start_date=form.cleaned_data.get('start_date')
            request.session['start_city']=start_city
            request.session['destination_city']=destination_city
            print(start_date)
            request.session['start_date']=str(start_date)


            print(start_date)
            buses=Bus.objects.all()
            print(buses)
            bus_list=[]
            for x in buses:
                if x.destination_city.lower()==destination_city.lower() and x.start_city.lower()==start_city.lower():
                    dates=bus_dates.objects.filter(bus=x)
                    dates1=[]
                    for d1 in dates:
                        dates1.append(d1.date.date())
                    if start_date in dates1:
                        d=x.costperkm * x.distance_from_startcity
                        t=x.reach-x.start
                        t1=t.days*24+t.seconds//3600
                        t2=(t.seconds % 3600) // 60

                        bus_list.append([x,d,x.start.time(),x.reach.time(),t1,t2])

                elif via.objects.filter(bus=x):
                    print('true1')
                    y=via.objects.filter(bus=x)
                    for z in y:
                        for a in y:
                            if z.place_name.lower()==start_city.lower() and a.place_name.lower()==destination_city.lower():
                                print('im true')
                                if (a.distance_from_startcity - z.distance_from_startcity) > 0:
                                    dates=bus_dates.objects.filter(bus=x)
                                    dates1=[]
                                    for d1 in dates:
                                        d2=d1.date+timedelta(minutes=z.journeytime)
                                        dates1.append(d2.date())
                                    print(dates1)
                                    if start_date in dates1:
                                        d=(x.costperkm) * (a.distance_from_startcity - z.distance_from_startcity)
                                        t=a.journeytime-z.journeytime
                                        t1=t//60
                                        t2=t%60
                                        bus_list.append([x,d,z.reach.time(),a.reach.time(),t1,t2])

                    for z in y:

                        if (x.start_city.lower()==start_city.lower() and z.place_name.lower()==destination_city.lower()) or (x.destination_city.lower()==destination_city.lower() and z.place_name.lower()==start_city.lower()):
                            if x.start_city.lower()==start_city.lower():
                                dates=bus_dates.objects.filter(bus=x)
                                dates1=[]
                                for d1 in dates:
                                    dates1.append(d1.date.date())
                                if start_date in dates1:
                                    d=(x.costperkm) * (z.distance_from_startcity)
                                    t=x.journeytime-z.journeytime
                                    t1=t//60
                                    t2=t % 60
                                    bus_list.append([x,d,x.start.time(),z.reach.time(),t1,t2])
                            elif x.destination_city.lower()==destination_city.lower():
                                print('true')
                                dates=bus_dates.objects.filter(bus=x)
                                dates1=[]
                                for d1 in dates:
                                    d2=d1.date+timedelta(minutes=z.journeytime)
                                    dates1.append(d2.date())
                                if start_date in dates1:
                                    d=(x.costperkm) * (x.distance_from_startcity - z.distance_from_startcity)
                                    t=x.journeytime-z.journeytime
                                    t1=t//60
                                    t2=t % 60

                                    bus_list.append([x,d,z.reach.time(),x.reach.time(),t1,t2])


            print(bus_list)
            return render(request,'bus_booking/search.html',{'bus':bus_list,'form':form} )


        else:
            print(form.errors)
            print('form1')
            form = bus_search()
            return render(request,'bus_booking/search.html',{'form':form,'bus':0})
    else:
        print('form')
        form = bus_search()
        return render(request,'bus_booking/search.html',{'form':form,'bus':0})

def test(request):
    if request.method == "POST":
        temp=request.POST["seats_text"]
        print(temp)
        return render(request,'bus_booking/passenger_details.html')
    else:
        ddata=[
          ["_x31_", '1',"1","1",'availabe','#fff'],
        [ "_x32_", "2","1","2",'availabe','#fff'],
        ["_x33_", "3","1","3",'availabe','#fff'],
        ["_x34_","4","1","4",'availabe','#fff'],
        ["_x35_","5","2","1",'availabe','#fff'],
        ["_x36_","6","2","2",'availabe','#fff'],
        ["_x37_","7","2","3",'availabe','#fff'],
        ["_x38_","8","2","4",'availabe','#fff'],
        ["_x39_", "9","3","1",'availabe','#fff'],
        ["_x31_0","10","3","2",'availabe','#fff'],
        ["_x31_1","11","3","3",'availabe','#fff'],
        ["_x31_2","12","3","4",'availabe','#fff'],
        ["_x31_3","13","4","1",'availabe','#fff'],
        [ "_x31_4","14","4","2",'availabe','#fff'],
        ["_x31_5","15","4","3",'availabe','#fff'],
        [ "_x31_6", "16","4","4",'availabe','#fff'],
        ["_x31_7","17","5","1",'availabe','#fff'],
        ["_x31_8","18","5","2",'availabe','#fff'],
        [ "_x31_9","19","5","3",'availabe','#fff'],
        ["_x32_0", "20","5","4",'availabe','#fff'],
        ["_x32_1", "21","6","1",'availabe','#fff'],
        ["_x32_2","22","6","2",'availabe','#fff'],
        ["_x32_3","23","6","3",'availabe','#fff'],
        ["_x32_4",  "24","6","4",'availabe','#fff'],
        ["_x32_5","25","7","1",'availabe','#fff'],
        ["_x32_6","26","7","2",'availabe','#fff'],
        ["_x32_7","27","7","3",'availabe','#fff'],
        [ "_x32_8", "28","7","4",'availabe','#fff'],
        ["_x32_9", "29","8","1",'availabe','#fff'],
        ["_x33_0","30","8","2",'availabe','#fff'],
        [ "_x33_1","31","8","3",'availabe','#fff'],
        ["_x33_2","32","8","4",'availabe','#fff'],
        [ "_x33_3","33","9","1",'availabe','#fff'],
        ["_x33_4","34","9","2",'availabe','#fff'],
         ["_x33_5","35","9","3",'availabe','#fff'],
        ["_x33_6","36","9","4",'availabe','#fff'],
        ["_x33_7", "37","10","1",'availabe','#fff'],
        ["_x33_8","38","10","2",'availabe','#fff'],
        ["_x33_9_1_","39","10","3",'availabe','#fff'],
        ["_x34_0", "40","10","4",'availabe','#fff'],

        ]

        json_list = json.dumps(ddata)
        return render(request,'bus_booking/try3.html',{'json_list':json_list})


def bus_detail(request,pk):
    ddata=[
              ["_x31_", '1',"1","1",'availabe','#fff'],
            [ "_x32_", "2","1","2",'availabe','#fff'],
            ["_x33_", "3","1","3",'availabe','#fff'],
            ["_x34_","4","1","4",'availabe','#fff'],
            ["_x35_","5","2","1",'availabe','#fff'],
            ["_x36_","6","2","2",'availabe','#fff'],
            ["_x37_","7","2","3",'availabe','#fff'],
            ["_x38_","8","2","4",'availabe','#fff'],
            ["_x39_", "9","3","1",'availabe','#fff'],
            ["_x31_0","10","3","2",'availabe','#fff'],
            ["_x31_1","11","3","3",'availabe','#fff'],
            ["_x31_2","12","3","4",'availabe','#fff'],
            ["_x31_3","13","4","1",'availabe','#fff'],
            [ "_x31_4","14","4","2",'availabe','#fff'],
            ["_x31_5","15","4","3",'availabe','#fff'],
            [ "_x31_6", "16","4","4",'availabe','#fff'],
            ["_x31_7","17","5","1",'availabe','#fff'],
            ["_x31_8","18","5","2",'availabe','#fff'],
            [ "_x31_9","19","5","3",'availabe','#fff'],
            ["_x32_0", "20","5","4",'availabe','#fff'],
            ["_x32_1", "21","6","1",'availabe','#fff'],
            ["_x32_2","22","6","2",'availabe','#fff'],
            ["_x32_3","23","6","3",'availabe','#fff'],
            ["_x32_4",  "24","6","4",'availabe','#fff'],
            ["_x32_5","25","7","1",'availabe','#fff'],
            ["_x32_6","26","7","2",'availabe','#fff'],
            ["_x32_7","27","7","3",'availabe','#fff'],
            [ "_x32_8", "28","7","4",'availabe','#fff'],
            ["_x32_9", "29","8","1",'availabe','#fff'],
            ["_x33_0","30","8","2",'availabe','#fff'],
            [ "_x33_1","31","8","3",'availabe','#fff'],
            ["_x33_2","32","8","4",'availabe','#fff'],
            [ "_x33_3","33","9","1",'availabe','#fff'],
            ["_x33_4","34","9","2",'availabe','#fff'],
             ["_x33_5","35","9","3",'availabe','#fff'],
            ["_x33_6","36","9","4",'availabe','#fff'],
            ["_x33_7", "37","10","1",'availabe','#fff'],
            ["_x33_8","38","10","2",'availabe','#fff'],
            ["_x33_9_1_","39","10","3",'availabe','#fff'],
            ["_x34_0", "40","10","4",'availabe','#fff'],


            ]

    if request.method == "POST":
        print('posted')

        temp=request.POST["seats_text"]
        print(temp)
        temp=temp.split(',')
        print(temp)
        for i in range(len(temp)):
            temp[i]=temp[i].split('-')
        print(temp)
        p=temp.pop()
        for i in temp:
            print(i[0])
        bus=Bus.objects.get(serviceno=request.session['pk'])
        viacount=via.objects.filter(bus=bus).count()
        print(viacount)
        vias=via.objects.filter(bus=bus).order_by('reach')
        print(vias)

        request.session['seat']=temp
        print(temp)
        j=0
        seats_selected=[]
        for i in temp:
            if i[1]=='selected':
                seats_selected.append(i[0])
                j=j+1
        print(j)
        request.session['noss']=j
        request.session['seats_selected']=seats_selected
        form = formset_factory(passenger_details, extra=j-1, min_num=1)
        conform=contactform()

        return render(request,'bus_booking/passenger_details.html',{'form':form,'contactaform':conform})

    elif pk:

        bus=Bus.objects.get(serviceno=pk)
        print(bus.start)
        vias=via.objects.filter(bus=pk).order_by('reach')
        print(vias)
        via_names=[]
        for a in vias:
            via_names.append(a.place_name.lower())
        if request.session['start_city'].lower()==bus.start_city.lower():

            dates=bus_dates.objects.filter(bus=bus)
            for d1 in dates:
                if request.session['start_date']==str(d1.date.date()):
                    request.session['bus_start_date']=str(d1.date.date())

            if request.session['destination_city'].lower()==bus.destination_city.lower():
                bookings=Bus_Booking.objects.filter(serviceno=pk,bus_start_date=request.session['start_date'])
            else:
                bookings=[]
                for a in vias:
                    if request.session['destination_city'].lower()==a.place_name.lower():
                        vias=list(vias)
                        index=vias.index(a)
                        booking=Bus_Booking.objects.filter(serviceno=pk,bus_start_date=request.session['start_date'])
                        for b in booking:
                            if b.start_city.lower() in via_names[index:]:
                                pass
                            else:
                                bookings.append(b)
        elif request.session['destination_city'].lower()==bus.destination_city.lower():
            bookings=[]
            for p in vias:
                if request.session['start_city'].lower()==p.place_name.lower():
                    dates=bus_dates.objects.filter(bus=bus)
                    for d1 in dates:
                        if request.session['start_date']==(d1.date + timedelta(p.journeytime)).date():
                            request.session['bus_start_date']=d1.date.date()


                    vias=list(vias)
                    index=vias.index(p)
                    booking=Bus_Booking.objects.filter(serviceno=pk,bus_start_date=request.session['bus_start_date'])
                    for b in booking:
                        if b.destination_city.lower() in via_names[:index+1]:
                            pass
                        else:
                            bookings.append(b)
        else:
            for p in vias:
                if request.session['start_city'].lower()==p.place_name.lower():
                    vias=list(vias)
                    index1=vias.index(p)
                    dates=bus_dates.objects.filter(bus=bus)
                    for d1 in dates:
                        if request.session['start_date']==(d1.date + timedelta(p.journeytime)).date():
                            request.session['bus_start_date']=d1.date.date()

            for q in vias:
                if request.session['destination_city'].lower()==q.place_name.lower():
                    vias=list(vias)
                    index2=vias.index(q)
            booking=Bus_Booking.objects.filter(serviceno=pk,bus_start_date=request.session['bus_start_date'])
            for b in booking:
                if b.start_city.lower() in via_names[:index1-1] or b.start_city.lower()==bus.start_city.lower():
                    if b.destination_city.lower() in via_names[:index1]:
                        pass
                elif b.start_city.lower() in via_names[index2:]:
                    pass
                else:
                    bookings.append(b)

        seats_booked=[]
        for a in bookings:
            b=passenger.objects.filter(booking_id=a)
            for c in b:
                seats_booked.append(c.seatno)
        print(seats_booked)
        for d in ddata:
            if d[1] in seats_booked:
                d[4]='booked'
        print('before converting')
        print(ddata)
        print('\n')
        for e in ddata[:]:
            if e[4]=='booked':
                print(e)
                ddata.remove(e)
        print('\n')
        print(ddata)
        request.session['data']=ddata
        request.session['pk']=pk
        request.session['seats_booked']=seats_booked
        json_list = json.dumps(ddata)

        return render(request,'bus_booking/bus_detail.html',{'json_list':json_list,'bus':bus})

# def bookingdetail(request,slug):
#     bookings=Bus_Booking.objects.get(booking_id=slug)
#     return render(request,'bus_booking/bookingdetail.html',{'bookings':bookings})


def mybookings(request):
    bookings=Bus_Booking.objects.filter(user=request.user)
    bookings=bookings[::-1]

    dicta={}
    for b in bookings:
        passengers=passenger.objects.filter(booking_id=b)
        dicta[b.booking_id]=passengers
    print(dicta)
    return render(request,'bus_booking/mybookings.html',{'bookings':bookings,'passengers':dicta})

def busticket(request):
    return render(request,'bus_booking/busticket.html')
