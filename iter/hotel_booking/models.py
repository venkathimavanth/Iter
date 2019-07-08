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
        print(self.images.all()[0].image.url)
        return self.images.all()[0].image.url

    def all_images(self):
        all_images = []
        for image in self.images.all():
            all_images.append(image.image.url)
        return all_images

    def __str__(self):
        return self.name

room_types = (
                ('Room','Room'),
                ("Standard Double Room","Standard Double Room"),
                ("Standard Family Room","Standard Family Room"),
                ("Deluxe Double Room","Deluxe Double Room")
)

room_facs = (
                ('AC','AC'),
                ('Non-AC','Non-AC')
)

class Rooms(models.Model):
    hotel_id=models.ForeignKey(Hotels, on_delete=models.CASCADE)
    room_type=models.CharField(default="Room",choices=room_types,max_length=30)
    room_fac=models.CharField(default="Non-AC",max_length=8,choices=room_facs)
    price=models.FloatField()
    cost=models.FloatField()
    availability=models.IntegerField(default=0)
    capacity=models.IntegerField(default=0)

    def __str__(self):
        return "{0} {1} {2}".format(self.hotel_id.name,self.room_type,self.room_fac)

class Hotel_Booking(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    gender=models.CharField(max_length=10)
    age=models.IntegerField()
    room_type=models.CharField(default="Room", max_length = 30)
    room_fac=models.CharField(default="Non-AC", max_length = 8)
    fromdate=models.DateField()
    fromtime=models.CharField(max_length=20)
    todate=models.DateField()
    totime=models.CharField(max_length=20)
    hotel=models.ForeignKey(Hotels, on_delete=models.CASCADE)
    booking_id=models.CharField(max_length=50)

    def __str__(self):
        return "{0} {1} {2} {3}".format(self.user.username,self.hotel.name,self.fromdate,self.todate)

class Image(models.Model):
    image = models.ImageField(upload_to='hotels',blank=True,null=True)
    hotel = models.ForeignKey(Hotels,on_delete=models.CASCADE,related_name='images')

    def __str__(self):
        return self.hotel.name

class Comments(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotels,on_delete=models.CASCADE)
    comment = models.TextField(blank = True)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return "{0} {1}".format(self.user.username,self.hotel.name)
