from django.shortcuts import render
from .distance_time_position import *
from django.http import HttpResponse
from .models import *

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
    for p in places:
        place_address=p.name + " " + p.city + " " + p.state + " " + p.country
        place_details.append(place_address)
        open_close_stay_preferred.append((p.open_time,p.close_time,p.stay_time,p.preferred_time))
    path_planing(place_details,open_close_stay_preferred,p.city,p.state,p.country)

    context={}
    return render(request,'trip_planner/plans.html',context)


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

    print(clusters)
    #print(start)

    clusters_sp=[]
    for c in clusters:
        temp=[]
        for p in c:
            temp.append((ocsp_temp[p][2],ocsp_temp[p][3]))
        clusters_sp.append(temp)
    #print(clusters_sp)

    cluster_path=[]

    for c in range(0,len(clusters)):
        completed=[]
        t=8
        while len(completed) != len(clusters[c]):
            t=t+1
            if t >= 25:
                t=1
            pos = -1
            for d in range(0,len(clusters[c])):
                if clusters_sp[c][d][1] == t and clusters[c][d] not in completed:
                    t=t+clusters_sp[c][d][0]-1
                    completed.append(clusters[c][d])
                    break
        cluster_path=cluster_path+completed
    print(cluster_path)


    #least time path
    positions=[]
    for i in range(0,len(distmatrix)):
        positions.append(i)

    least_time_path=[]
    time=7
    '''
    while len(least_time_path) != len(positions):
        if time>=24:
            time=1
        temp=list(set(positions)-set(least_time_path)).sort()
        ocsp_not_completed=[]
        for i in temp:
            t=[]
            for j in temp:
                t.append(ocsp_temp[i][j])
            ocsp_not_completed.append(t)
'''


















'''
    min=100
    max=0
    su=0
    for i in ocsp_temp:
        su=su+i[2]
        if min > i[2]:
            min=i[2]
        if max < i[2]:
            max=i[2]
    days=math.ceil((su/10.0))
    day=[]
    for i in range(days):
        least_time_path.append([])
        day.append(['........................'])

    for i in range(max,min-1,-1):
        for j in range(0,ocsp_temp):
            if ocsp_temp[j][1]:
                pass
    '''




    #while len(least_time_path) != len(positions):
















#end
