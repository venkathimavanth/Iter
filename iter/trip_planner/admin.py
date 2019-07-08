from django.contrib import admin

from .models import Trip,Place,Distances,TripDetails
# Register your models here.
admin.site.register(Place)
admin.site.register(Trip)
admin.site.register(Distances)
admin.site.register(TripDetails)
