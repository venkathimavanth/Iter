from django.shortcuts import render
from .distance_time_position import *
from django.http import HttpResponse
from .models import *

import itertools
import copy
import math
# Create your views here.



def trip_plan(request):
    places=Place.objects.all()
    place_details=[]
    open_close_stay_preferred=[]
    for p in places:
        place_address=p.name + " " + p.city + " " + p.state + " " + p.country
        place_details.append(place_address)
        open_close_stay_preferred.append((p.open_time,p.close_time,p.stay_time,p.preferred_time))
    path_planing(place_details,open_close_stay_preferred,p.city,p.state,p.country)

    return HttpResponse("Places")


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

    #print(clusters)
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
    #print(cluster_path)


    #least time path
    positions=[]
    for i in range(0,len(distmatrix)):
        positions.append(i)

    least_time_path=[]
    time=7
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
