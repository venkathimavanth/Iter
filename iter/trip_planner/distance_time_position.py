import herepy


#get latitude and longitude
def get_lat_long(place):

    search_string="DisplayPosition"
    lat=0.0
    long=0.0
    trig=0

    try:
        geocoderApi = herepy.GeocoderApi('dy8kVG3quHsuzvzE2IPe', 'krzVA06TkOKIp6Km2Jkdiw')
        response = geocoderApi.free_form(place)

        response=str(response)
        reslen=len(response)

        try:
            for i in range(len(search_string),reslen):
                if response[i-len(search_string):i]=="DisplayPosition":
                    la=response[i+16:i+24]
                    lo=response[i+39:i+47]
                    lat=float(la)
                    long=float(lo)
                    trig=1
        except:
            trig=0
    except:
        trig=-1
    return (trig,lat,long)


#get distance and time to travel
def get_distance_timetotravel(start,dest):
    trig=0
    print(start,  '---to---' ,dest, "  : ",end="")
    start=get_lat_long(start)
    dest=get_lat_long(dest)
    numbers=['0','1','2','3','4','5','6','7','8','9',]
    travel_time=0
    traffic_time=0
    distance=0
    if start[0]==dest[0]==1:
        dist_string="The trip takes"

        try:
            routingApi = herepy.RoutingApi('dy8kVG3quHsuzvzE2IPe', 'krzVA06TkOKIp6Km2Jkdiw')
            response = routingApi.car_route([start[1] ,start[2]],
                                                   [dest[1] ,dest[2]],
                                                   [herepy.RouteMode.car, herepy.RouteMode.fastest])

            response=str(response)
            reslen=len(response)


            for i in range(reslen,10,-1):
                if response[i-10:i]=="travelTime":
                    time=""
                    for j in range(i+3,i+10):
                        if response[j] not in numbers:
                            break
                        time=time+response[j]
                    travel_time=int(time)
                    break

            for i in range(reslen,11,-1):
                if response[i-11:i]=="trafficTime":
                    time=""
                    for j in range(i+3,i+10):
                        if response[j] not in numbers:
                            break
                        time=time+response[j]
                    traffic_time=int(time)
                    break

            for i in range(reslen,len(dist_string),-1):
                if response[i-len(dist_string):i]=="The trip takes":
                    dist=""
                    for j in range(i+24,i+34):
                        if response[j]=='k':
                            break
                        dist=dist+response[j]
                    distance=float(dist)
                    break
            trig=1
        except:
            trig=0
    print(distance , "," ,trig)
    return(trig,distance,travel_time,traffic_time)




#start='jntu kukatpally hyderabad'
#dest='bjp office kukatpally hyderabad'
#t=get_distance_timetotravel(start,dest)
#print(t)
