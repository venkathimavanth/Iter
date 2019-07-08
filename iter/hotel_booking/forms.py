from django import forms
from .models import Comments,Hotel_Booking

class hotel_search(forms.Form):
    city_name=forms.CharField(min_length=1,max_length=100,required=True,widget=forms.TextInput(),label='')
    From=forms.DateField(required=True,widget=forms.DateInput(),label="")
    To=forms.DateField(label="",widget=forms.DateInput(),required=True)

    class Meta:
        fields = ['city_name','From','To']

class Mycomments(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['comment']

class Book(forms.Form):
    class Meta:
        model = Hotel_Booking
        fields = '__all__'
