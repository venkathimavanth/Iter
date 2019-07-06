from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

# Create your models here.
class Hotels(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    hotel_id=models.AutoField(primary_key=True)
    address=models.CharField( max_length=300,null=True)
    city=models.CharField( max_length=30,null=True)
    state=models.CharField( max_length=30,null=True)
    country=models.CharField( max_length=30,null=True)
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
    description = models.CharField(max_length=1000,default="Hello")
    lat = models.FloatField(default = 0)
    long = models.FloatField(default = 0)

    def get_absolute_url(self):
        return reverse('hotel_detail',kwargs={'id' : self.id})

    def first_image(self):
        return self.images.all()[0].image.url

    def all_images(self):
        all_images = []
        for image in self.images.all():
            all_images.append(image.image.url)
        return all_images

    def __str__(self):
        return self.name

class Rooms(models.Model):
    hotel_id=models.ForeignKey(Hotels, on_delete=models.CASCADE)
    room_type=models.IntegerField(default=1)
    room_fac=models.IntegerField(default=1)
    price=models.FloatField()
    cost=models.FloatField()
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

class Image(models.Model):
    image = models.ImageField(upload_to='hotels')
    hotel = models.ForeignKey(Hotels,on_delete=models.CASCADE,related_name='images')

    def __str__(self):
        return self.hotel.name

class Comments(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotels,on_delete=models.CASCADE)
    comment = models.TextField(blank = True)
    rating = models.IntegerField(default=0)
