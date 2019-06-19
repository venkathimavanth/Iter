from django import forms
from bus_booking.models  import passenger


class passenger_details():
        gender_choice = (
            ('Male','Male'),
            ('Female', 'Female'),
            ('others', 'others'),

                                )
        name=forms.CharField(min_length=1,max_length=100,required=True,widget=forms.TextInput())
        gender=forms.ChoiceField(choices = gender_choice, label="", initial='', widget=forms.Select(), required=True)
        age=forms.IntegerField()


    class Meta:
        model = passenger
        fields = ['name','gender','age']
