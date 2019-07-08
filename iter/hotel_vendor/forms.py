from django import forms
from django.forms import ClearableFileInput
from hotel_booking.models  import Hotels,Rooms,Image

class hotel_details(forms.Form):
    name=forms.CharField(min_length=1,max_length=100,required=True,widget=forms.TextInput())
    address=forms.CharField(min_length=1,max_length=100,required=True,widget=forms.TextInput())
    city=forms.CharField(min_length=1,max_length=100,required=True,widget=forms.TextInput())
    state=forms.CharField(min_length=1,max_length=100,required=True,widget=forms.TextInput())
    country=forms.CharField(min_length=1,max_length=100,required=True,widget=forms.TextInput())
    phone_number = forms.CharField(min_length=1, max_length=100, required=True, widget=forms.TextInput())
    email=forms.EmailField()


    class Meta:
        model = Hotels
        fields = ['name', 'address','city','state','country','phone_number']

class room_details(forms.Form):

    room_type_choice = (
        ('4','UltaDeluxe'),
        ('3','Standard'),
        ('2', 'Deluxe'),
        ('1', 'Suite'),

                            )

    room_fac_choice = (
        ('2', 'AC'),
        ('1', 'Non AC'),

                            )

    room_type=forms.ChoiceField(choices = room_type_choice, label="", initial='', widget=forms.Select(), required=True)
    room_fac=forms.ChoiceField(choices = room_fac_choice, label="", initial='', widget=forms.Select(), required=True)
    cost=forms.FloatField(required=True,widget=forms.TextInput())
    price=forms.FloatField(required=True,widget=forms.TextInput())
    availability=forms.IntegerField(required=True,widget=forms.TextInput())
    capacity=forms.IntegerField(required=True,widget=forms.TextInput())

    class Meta:
        model = Rooms
        fields = ['room_type','room_fac','cost','price','availability','capacity']

#class AddhotelForm(forms.ModelForm):
#    class Meta:
#        model = Image
#        fields = ['image']
#        widgets = {
#            'image': ClearableFileInput(attrs={'multiple': True}),
#        }
