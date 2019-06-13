from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Bus_agency(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    agent_id=models.AutoField(primary_key=True)

    address=models.CharField( max_length=300)
    phone_number= models.CharField(max_length=10,
                                    validators=[
                                        RegexValidator(
                                            regex='^[1-9]{1}[0-9]{9}$',
                                            message='Enter a valid phone number',
                                            code='invalid_cell'
                                        ),
                                    ]
                                    )
    email=models.EmailField(max_length=70, null=True, blank=True, unique=True)

class Bus(models.Model):
        agency=models.ForeignKey(Bus_agency, on_delete=models.CASCADE)
        Bus_type=models.IntegerField(default=1)
        costperkm=models.FloatField()
        serviceno=models.IntegerField()
        noseats=models.IntegerField(default=0)
        start_city=models.CharField(max_length=50)
        destination_city=models.CharField(max_length=50)

class Seats(models.Model):
    Bus=models.ForeignKey(Bus,on_delete=models.CASCADE)
    seatside=models.CharField(max_length=50)
    seatno=models.IntegerField()


class Bus_Booking(models.Model):
        user=models.ForeignKey(User, on_delete=models.CASCADE)
        name=models.CharField(max_length=100)
        gender=models.CharField(max_length=1)
        age=models.IntegerField()
        bus_type=models.IntegerField(default=1)
        journeydate=models.DateField()
        journeytime=models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(1440)])
        reachdate=models.DateField()
        reachtime=models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(1440)])
        agency_id=models.ForeignKey(Bus_agency, on_delete=models.CASCADE)
        serviceno=models.IntegerField()
        booking_id=models.CharField(max_length=10)
        seatno=models.CharField(max_length=5)
