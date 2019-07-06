from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
# Create your models here.
class Place(models.Model):

    name=models.CharField(primary_key=True, max_length=100)
    Description=models.CharField(max_length=500)
    city=models.CharField( max_length=100)
    country=models.CharField( max_length=100)
    state=models.CharField( max_length=10)
    rating=models.IntegerField()
    open_time=models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(24)])
    close_time=models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(24)])
    stay_time=models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(24)])
    preferred_time=models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(24)])
    pic=models.ImageField(upload_to="places",default="places/default.jpg")

class Trip(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    Trip_id=models.AutoField(primary_key=True)
    Description=models.CharField( max_length=1000)
    plan = models.CharField(max_length=1000)
    start_date=models.DateField()
    end_date=models.DateField()
    start_time=models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(1440)])
    end_time=models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(1440)])

class Distances(models.Model):
    start=models.CharField(max_length=200)
    dest=models.CharField(max_length=200)
    distance=models.FloatField(default=0)
    time=models.FloatField(default=0)
    city=models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    country=models.CharField(max_length=50)
