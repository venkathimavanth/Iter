from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse

# Create your models here.
class Bus_agency(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=100,unique=True)
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
        bus_type_choice = (
        ('Sleeper', 'Sleeper'),
        ('Semi Sleeper', 'Semi Sleeper'),
        ('Seater', 'Seater'),



                            )
        bus_model_choice = (
        ('scania','scania'),
        ('volvo', 'volvo'),
        ('super luxary', 'super luxary'),

        ('Normal', 'Normal'),

                            )


        Bus_type=models.CharField(choices=bus_type_choice,max_length=20)
        Bus_model=models.CharField(choices=bus_model_choice,max_length=20,null=True)
        serviceno=models.IntegerField(primary_key=True)
        distance_from_startcity=models.FloatField(default=600)
        costperkm=models.FloatField()
        noseats=models.IntegerField(default=40)
        start_city=models.CharField(max_length=50)
        destination_city=models.CharField(max_length=50)
        seats_available=models.CharField(max_length=1000,default='?'*1000)
        start=models.DateTimeField(null=True, blank=True)
        reach=models.DateTimeField(null=True, blank=True)
        date=models.DateField()
        journeytime=models.IntegerField(null=True)

        def get_absolute_url(self):
            return reverse('bus_detail',kwargs={'id' : self.id})



class via(models.Model):
    bus=models.ForeignKey(Bus,on_delete=models.CASCADE)
    place_name=models.CharField(max_length=100)
    distance_from_startcity=models.FloatField()
    reach=models.DateTimeField(null=True, blank=True)
    journeytime=models.IntegerField(null=True)

class bus_dates(models.Model):
    bus=models.ForeignKey(Bus,on_delete=models.CASCADE)
    date=models.DateTimeField()
#    booking=models.ForeignKey('Bus_Booking',on_delete=SET_NULL)


class Bus_Booking(models.Model):
        user=models.ForeignKey(User,null=True, on_delete=models.CASCADE)
        bus_type=models.CharField(max_length=20)
        Bus_model=models.CharField(max_length=20,null=True)
        start_city=models.CharField(max_length=50)
        destination_city=models.CharField(max_length=50)
        bus_start_date=models.DateField()
        start=models.DateTimeField(null=True, blank=True)
        reach=models.DateTimeField(null=True, blank=True)
        serviceno=models.ForeignKey(Bus,on_delete=models.CASCADE)
        booking_id=models.CharField(max_length=20,primary_key=True)
        fare=models.FloatField(default='1000.0')
        email=models.EmailField(default='koushiks666@gmail.com')
        phone_number = models.CharField(max_length=10,default='8179033301',
                                    validators=[
                                        RegexValidator(
                                            regex='^[1-9]{1}[0-9]{9}$',
                                            message='Enter a valid phone number',
                                            code='invalid_cell'
                                        ),
                                    ]
                                    )

class passenger(models.Model):
        gender_choice = (
                ('Male','Male'),
                ('Female', 'Female'),
                ('others', 'others'),

                                    )

        booking_id=models.ForeignKey(Bus_Booking, on_delete=models.CASCADE)
        name=models.CharField(max_length=100)
        gender=models.CharField(choices=gender_choice,max_length=6)
        age=models.IntegerField()
        seatno=models.CharField(max_length=5,default=1)
