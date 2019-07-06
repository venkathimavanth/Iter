from django.contrib import admin
from .models import Bus_agency,Bus,Bus_Booking,via,passenger,bus_dates
# Register your models here.
admin.site.register(Bus_agency)
admin.site.register(Bus)
admin.site.register(Bus_Booking)
admin.site.register(via)
admin.site.register(passenger)
admin.site.register(bus_dates)
