from django import forms
from bus_booking.models  import passenger


class passenger_details(forms.Form):
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

class bus_search(forms.Form):
    start_city=forms.CharField(min_length=1,max_length=100,required=True,widget=forms.TextInput(),label='')
    destination_city=forms.CharField(min_length=1,max_length=100,required=True,widget=forms.TextInput(),label="")
    start_date=forms.DateField(label="",widget=forms.DateInput())


    class Meta:
        fields = ['start_city','destination_city','start_date']
