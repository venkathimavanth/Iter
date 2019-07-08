from django.shortcuts import render
from .distance_time_position import *
from django.http import HttpResponse
from .models import *
from hotel_booking.models import *
from math import sin, cos, sqrt, atan2, radians


import itertools
import copy
import math
# Create your views here.

def trip_home(request):
    places=Place.objects.all()
    places_list=[]
    for p in places:
        places_list.append(p.city)
    places_set=set(places_list)
    places_list=list(places_set)
    places_list.sort()
    context ={'places_list':places_list,}
    return render(request,'trip_planner/home.html',context)

def my_plans(request):
    my_iters=[]
    plans=Trip.objects.all().reverse()
    for p in plans:
        details=[p.city,p.plan,p.days]
        temp=[]
        plan_details=TripDetails.objects.filter(Trip_id=p.Trip_id)
        for pd in plan_details:
            temp.append((pd.detail_type,pd.detail))
            # print("hello")
        details.append(temp)
        my_iters.append(details)
        # print(my_iters)
        my_iters.reverse()
    context={"my_iters":my_iters}
    return render(request,'trip_planner/my_plans.html',context)

def save_my_plan(request,value):
    t=temp(request)
    user=request.user
    city=request.session['city']
    plan=""
    days=0
    l=[]
    print(type(value))
    if value == '2':
        plan="Rushed ITER"
        days=t["rushed_days"]
        l=t["rushed_final_list"]
    elif value =='1':
        plan="Relaxed ITER"
        days=t["cluster_days"]
        l=t["cluster_final_list"]
    elif value =='3':
        plan="Economic ITER"
        days=t["economic_days"]
        l=t["economic_final_list"]
    trip=Trip(user=user,city=city,days=days,plan=plan)
    trip.save()
    for i in l:
        tripdetails=TripDetails(Trip_id=trip.Trip_id,detail_type=i[0],detail=i[1])
        tripdetails.save()

    return my_plans(request)
    # return HttpResponse("pages")


def trip_city(request,value):
    request.session['city'] = value
    places=Place.objects.filter(city=value)
    c=0
    for p in places:
        c=c+1
        p.Description=(p.Description).upper()
        p.name=(p.name).upper()
    image_width=1100/c + 40/c
    context={"places":places,"value":value.upper(),"count":c,"image_width":image_width}
    return render(request,'trip_planner/placesbycity.html',context)

def trip_plan(request):
    city=request.session['city']
    selected_place_no=request.POST['final-list']
    request.session['selected_place_no']=request.POST['final-list']
    selected_places=[]
    selected_place_no=selected_place_no.split(',')
    selected_place_no=selected_place_no[0:len(selected_place_no)-1]
    for s in selected_place_no:
        selected_places.append(int(s[-1]))
    places=Place.objects.filter(city=city)
    places_temp=[]
    i=1
    for p in places:
        if i in selected_places:
            places_temp.append(p)
            # print(i,selected_places)
        i=i+1
    places=places_temp

    place_details=[]
    open_close_stay_preferred=[]
    place=[]
    for p in places:
        place.append(p)
        place_address=p.name + " " + p.city + " " + p.state + " " + p.country
        place_details.append(place_address)
        open_close_stay_preferred.append((p.open_time,p.close_time,p.stay_time,p.preferred_time))

    a,b=path_planing(place_details,open_close_stay_preferred,p.city,p.state,p.country)
    # print(a)
    hotels=Hotels.objects.filter(city=city)
    cluster_hotels=[]
    for i in a[0]:
        lat=0
        long=0
        for j in i:
            temp=get_lat_long(place_details[j])
            lat=lat+temp[1]
            long=long+temp[2]
        lat=lat/len(i)
        long=long/len(i)
        # print(lat,long)
        best=Hotels.objects.filter(name="default")
        dist=distance(lat,long,0,0)
        for h in hotels:
            d=distance(lat,long,h.lat,h.long)
            if d <= dist :
                dist=d
                best=h
        cluster_hotels.append(best)

    rushed_hotel=[]
    lat=0
    long=0
    for i in place_details:
        temp=get_lat_long(i)
        lat=lat+temp[1]
        long=long+temp[2]
    lat=lat/len(place_details)
    long=long/len(place_details)
    best=Hotels.objects.filter(name="default")
    dist=distance(lat,long,0,0)
    for h in hotels:
        d=distance(lat,long,h.lat,h.long)
        if d <= dist :
            dist=d
            best=h
    rushed_hotel.append(best)
    # print(eco_hotel,cluster_hotels)

    t=0
    cluster_final_list=[]
    day=1
    for i in a[0]:
        cluster_final_list.append((1,"Day - " +str(day)))
        for c in cluster_hotels[a[0].index(i)]:
            s="Stay At Hotel " + c.name + " , " + c.city
            cluster_final_list.append((2,s,c))
            # print(c.name)

        for j in range(0,len(i)):
            start=open_close_stay_preferred[a[1][t]][3]
            end=open_close_stay_preferred[a[1][t]][3] +open_close_stay_preferred[a[1][t]][2]
            p=str(start) + ":00 - " + str(end) + ":00     >  " + " Visit " + place[a[1][t]].name
            cluster_final_list.append((3,p))
            t=t+1
        day=day+a[3][a[0].index(i)]
    d1=str(sum(a[3])) + " Days Plan "
    # print(sum(a[3]))


    print(b)
    rushed_final_list=[]
    day=1
    h="Stay At Hotel "
    for rush in rushed_hotel[0]:
        h=h+rush.name + " , " + rush.city + " Through Out The Tour"
        rushed_final_list.append((2,h,rush))
    rushed_final_list.append((1,"Day - " +str(day)))
    day=day+1
    for i in b:
        if i == '-':
            rushed_final_list.append((1,"Day - " +str(day)))
            day=day+1
        else:
            stay=open_close_stay_preferred[i][2]
            p="For " + str(stay) +  " Hours  >  " + " Visit " + place[i].name
            rushed_final_list.append((3,p))
    d2=str(day-1) + " Days Plan "
    economic_final_list=copy.deepcopy(rushed_final_list)
    context={"cluster_final_list":cluster_final_list,"cluster_days":d1,"rushed_final_list":rushed_final_list,"rushed_days":d2,"economic_final_list":economic_final_list,"economic_days":d2}
    # request.session['context'] = context
    # print(request.session['context'])
    return render(request,'trip_planner/plans.html',context)


def distance(a,b,c,d):
    R = 6373.0
    lat1 = radians(a)
    lon1 = radians(b)
    lat2 = radians(c)
    lon2 = radians(d)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    # print(distance)
    return distance

def path_planing(place_details,ocsp,city,state,country):
    place_details=place_details
    ocsp=ocsp
    place_details_temp=copy.deepcopy(place_details)
    ocsp_temp=copy.deepcopy(ocsp)
    distmatrix=[]


    for i in range(0,len(place_details_temp)):
        temp=[]
        for j in range(0,len(place_details_temp)):
            temp.append(0)
        distmatrix.append(temp)
    timematrix=[]
    for i in range(0,len(place_details_temp)):
        temp=[]
        for j in range(0,len(place_details_temp)):
            temp.append(0)
        timematrix.append(temp)


    for i in range(0,len(place_details_temp)):
        for j in range(i+1,len(place_details_temp)):
            if Distances.objects.filter(start=place_details_temp[i]).filter(dest=place_details_temp[j]).filter(city=city).filter(state=state).filter(country=country).count() == 0 :
                t=get_distance_timetotravel(place_details_temp[i],place_details_temp[j])
                if t[0] ==1:
                    Distances.objects.create(start=place_details_temp[i],dest=place_details_temp[j],city=city,state=state,country=country,distance=float(t[1]),time=t[2])
                    Distances.objects.create(start=place_details_temp[j],dest=place_details_temp[i],city=city,state=state,country=country,distance=float(t[1]),time=t[2])
            for o in Distances.objects.filter(start=place_details_temp[i]).filter(dest=place_details_temp[j]).filter(city=city).filter(state=state).filter(country=country):
                distmatrix[i][j]=distmatrix[j][i]=o.distance
                timematrix[i][j]=timematrix[j][i]=o.time
        #print(distmatrix[i])


#cluster planing
    positions=[]
    for i in range(0,len(distmatrix)):
        positions.append(i)

    clusters=[]
    start=[]
    while len(positions):
        temp_distmatrix=[]
        for i in positions:
            temp=[]
            for j in positions:
                temp.append(distmatrix[i][j])
            temp_distmatrix.append(temp)

        pos=0
        su=sum(temp_distmatrix[pos])
        for i in range(1,len(temp_distmatrix)):
            if sum(temp_distmatrix[i]) < su:
                su=sum(temp_distmatrix[i])
                pos=i
        start.append(pos)
        temp=[]
        for i in range(0,len(positions)):
            if temp_distmatrix[pos][i]<=10:
                temp.append(positions[i])
        positions=list(set(positions)-set(temp))
        positions.sort()
        clusters.append(temp)

    # print(clusters)
    # print(start)

    clusters_sp=[]
    for c in clusters:
        temp=[]
        for p in c:
            temp.append((ocsp_temp[p][2],ocsp_temp[p][3]))
        clusters_sp.append(temp)
    #print(clusters_sp)

    cluster_path=[]
    day=[]
    cluster_days=0
    for c in range(0,len(clusters)):
        completed=[]
        t=8
        days=1
        while len(completed) != len(clusters[c]):
            d=0
            t=t+1
            if t >= 25:
                days=days+1
                t=1
                d=d+1
                # day.append('.')
            pos = -1
            for d in range(0,len(clusters[c])):
                if clusters_sp[c][d][1] == t and clusters[c][d] not in completed:
                    t=t+clusters_sp[c][d][0]-1
                    completed.append(clusters[c][d])
                    # day.append('-')
                    break
        day.append(d+1)
        cluster_days=cluster_days+days
        cluster_path=cluster_path+completed
    # day=day[0:len(day)-1]
    print(day)
    # print(clusters,cluster_path,cluster_days,day)


    #least time path
    positions=[]
    for i in range(0,len(distmatrix)):
        positions.append(i)

    least_time_path=[]
    time=7
    # print(ocsp_temp)
    while len(positions) != 0 :
        least=time+ocsp_temp[0][2]
        pos=0
        for i in range(len(positions)):
            if time+ocsp_temp[i][2] < least and ocsp_temp[i][1]>=time+ocsp_temp[i][2]:
                least=time+ocsp_temp[positions[i]][2]
                pos=i
        # print(least_time_path)
        # if (least <= ocsp_temp[positions[pos]][1]) and (least-ocsp_temp[positions[i]][2] >= ocsp_temp[positions[pos]][0]):
        least_time_path.append(positions[pos])
        time=least
        positions.pop(pos)
        # print(positions[i],least,ocsp_temp[positions[i]],pos)
        # else:
        time=time+1
        if time >=24:
            time=time-24
            least_time_path.append('-')
    # print(least_time_path)

    return((clusters,cluster_path,cluster_days,day),least_time_path)




def temp(request):
    city=request.session['city']
    selected_place_no=request.session['selected_place_no']
    selected_places=[]
    selected_place_no=selected_place_no.split(',')
    selected_place_no=selected_place_no[0:len(selected_place_no)-1]
    for s in selected_place_no:
        selected_places.append(int(s[-1]))
    places=Place.objects.filter(city=city)
    places_temp=[]
    i=1
    for p in places:
        if i in selected_places:
            places_temp.append(p)
            # print(i,selected_places)
        i=i+1
    places=places_temp

    place_details=[]
    open_close_stay_preferred=[]
    place=[]
    for p in places:
        place.append(p)
        place_address=p.name + " " + p.city + " " + p.state + " " + p.country
        place_details.append(place_address)
        open_close_stay_preferred.append((p.open_time,p.close_time,p.stay_time,p.preferred_time))

    a,b=path_planing(place_details,open_close_stay_preferred,p.city,p.state,p.country)
    # print(a)
    hotels=Hotels.objects.filter(city=city)
    cluster_hotels=[]
    for i in a[0]:
        lat=0
        long=0
        for j in i:
            temp=get_lat_long(place_details[j])
            lat=lat+temp[1]
            long=long+temp[2]
        lat=lat/len(i)
        long=long/len(i)
        # print(lat,long)
        best=Hotels.objects.filter(name="default")
        dist=distance(lat,long,0,0)
        for h in hotels:
            d=distance(lat,long,h.lat,h.long)
            if d <= dist :
                dist=d
                best=h
        cluster_hotels.append(best)

    rushed_hotel=[]
    lat=0
    long=0
    for i in place_details:
        temp=get_lat_long(i)
        lat=lat+temp[1]
        long=long+temp[2]
    lat=lat/len(place_details)
    long=long/len(place_details)
    best=Hotels.objects.filter(name="default")
    dist=distance(lat,long,0,0)
    for h in hotels:
        d=distance(lat,long,h.lat,h.long)
        if d <= dist :
            dist=d
            best=h
    rushed_hotel.append(best)
    # print(eco_hotel,cluster_hotels)

    t=0
    cluster_final_list=[]
    day=1
    for i in a[0]:
        cluster_final_list.append((1,"Day - " +str(day)))
        for c in cluster_hotels[a[0].index(i)]:
            s="Stay At Hotel " + c.name + " , " + c.city
            cluster_final_list.append((2,s,c))
            # print(c.name)

        for j in range(0,len(i)):
            start=open_close_stay_preferred[a[1][t]][3]
            end=open_close_stay_preferred[a[1][t]][3] +open_close_stay_preferred[a[1][t]][2]
            p=str(start) + ":00 - " + str(end) + ":00     >  " + " Visit " + place[a[1][t]].name
            cluster_final_list.append((3,p))
            t=t+1
        day=day+a[3][a[0].index(i)]
    d1=str(sum(a[3])) + " Days Plan "
    # print(sum(a[3]))


    print(b)
    rushed_final_list=[]
    day=1
    h="Stay At Hotel "
    for rush in rushed_hotel[0]:
        h=h+rush.name + " , " + rush.city + " Through Out The Tour"
        rushed_final_list.append((2,h,rush))
    rushed_final_list.append((1,"Day - " +str(day)))
    day=day+1
    for i in b:
        if i == '-':
            rushed_final_list.append((1,"Day - " +str(day)))
            day=day+1
        else:
            stay=open_close_stay_preferred[i][2]
            p="For " + str(stay) +  " Hours  >  " + " Visit " + place[i].name
            rushed_final_list.append((3,p))
    d2=str(day-1) + " Days Plan "
    economic_final_list=copy.deepcopy(rushed_final_list)
    context={"cluster_final_list":cluster_final_list,"cluster_days":d1,"rushed_final_list":rushed_final_list,"rushed_days":d2,"economic_final_list":economic_final_list,"economic_days":d2}
    return context











#end
