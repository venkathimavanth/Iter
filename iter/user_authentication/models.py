from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.validators import RegexValidator

# Create your models here.
class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture=models.ImageField(upload_to='profile_image', default='static/userlogin/images/default-img.png')
    phone_number = models.CharField(max_length=10,
                                    validators=[
                                        RegexValidator(
                                            regex='^[1-9]{1}[0-9]{9}$',
                                            message='Enter a valid phone number',
                                            code='invalid_cell'
                                        ),
                                    ]
                                    )
    user_choice = (
        ('B', 'bus_client'),
        ('C', 'Customer'),
        ('H','hotel_client')
    )
    user_type=models.CharField(choices=user_choice, max_length=2, default='C')
    signedup_time=models.DateTimeField(auto_now_add=True)
    email_confirmed = models.BooleanField(default=False)



    def __str__(self):  # __unicode__ for Python 2
        return self.user.username
