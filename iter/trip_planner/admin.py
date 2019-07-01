from django.contrib import admin

from .models import Trip,Place,Distances
# Register your models here.
admin.site.register(Place)
admin.site.register(Trip)
admin.site.register(Distances)
