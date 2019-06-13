from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

# Create your models here.
class Hotels(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    hotel_id=models.AutoField(primary_key=True)
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


class Rooms(models.Model):
    hotel_id=models.ForeignKey(Hotels, on_delete=models.CASCADE)
    room_type=models.IntegerField(default=1)
    cost=models.FloatField()
    discount=models.FloatField()
    availability=models.IntegerField(default=0)
    capacity=models.IntegerField(default=0)

class Hotel_Booking(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    
    name=models.CharField(max_length=100)
    gender=models.CharField(max_length=1)
    age=models.IntegerField()
    room_type=models.IntegerField(default=1)
    fromdate=models.DateField()
    fromtime=models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(1440)])
    todate=models.DateField()
    totime=models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(1440)])
    hotel_id=models.ForeignKey(Hotels, on_delete=models.CASCADE)
    booking_id=models.CharField(max_length=20)
