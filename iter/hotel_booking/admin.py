from django.contrib import admin

from .models import Hotels,Rooms,Hotel_Booking,Image,Comments
# Register your models here.
admin.site.register(Hotels)
admin.site.register(Rooms)
admin.site.register(Hotel_Booking)
admin.site.register(Image)
admin.site.register(Comments)
