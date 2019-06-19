from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

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
        ('Normal', 'Normal'),

                            )
        bus_model_choice = (
        ('scania','scania'),
        ('volvo', 'volvo'),
        ('Normal', 'Normal'),

                            )


        Bus_type=models.CharField(choices=bus_type_choice,max_length=20)
        Bus_model=models.CharField(choices=bus_model_choice,max_length=20,null=True)
        serviceno=models.IntegerField(primary_key=True)
        costperkm=models.FloatField()
        noseats=models.IntegerField(default=0)
        start_city=models.CharField(max_length=50)
        destination_city=models.CharField(max_length=50)
        seats_available=models.CharField(max_length=60,default='?'*1000)
        journeydate=models.DateField()
        start_time=models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(1440)],default=0)
        reach_time=models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(1440)],default=0)
        reachdate=models.DateField()

class via(models.Model):
    bus=models.ForeignKey(Bus,on_delete=models.CASCADE)
    place_name=models.CharField(max_length=100)
    reach_date=models.DateField()
    reach_time=models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(1440)])
    start_date=models.DateField()
    start_time=models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(1440)])
    distance_from_startcity=models.FloatField()



class Bus_Booking(models.Model):
        user=models.ForeignKey(User, on_delete=models.CASCADE)
        bus_type=models.IntegerField(default=1)
        journeydate=models.DateField(null=True)
        journeytime=models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(1440)])
        reachdate=models.DateField(null=True)
        reachtime=models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(1440)])
        agency_id=models.ForeignKey(Bus_agency, on_delete=models.CASCADE)
        serviceno=models.IntegerField()
        booking_id=models.CharField(max_length=20,primary_key=True)
        noofseats=models.CharField(max_length=5,default=1)
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
