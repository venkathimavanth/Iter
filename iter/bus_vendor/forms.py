from django import forms
from bus_booking.models  import Bus_agency,Bus,via

class agency_details(forms.Form):

    name=forms.CharField(min_length=1,max_length=100,required=True,widget=forms.TextInput())
    address=forms.CharField(min_length=1,max_length=100,required=True,widget=forms.TextInput())
    phone_number = forms.CharField(min_length=1, max_length=100, required=True, widget=forms.TextInput())
    email=forms.EmailField()

    class Meta:
        model = Bus_agency
        fields = ['name','address','phone_number','email']

class bus_details(forms.Form):
    bus_type_choice = (
        ('Sleeper', 'Sleeper'),
        ('Normal', 'Normal'),

                            )
    bus_model_choice = (
        ('scania','scania'),
        ('volvo', 'volvo'),
        ('Normal', 'Normal'),

                            )
    bus_type=forms.ChoiceField(choices = bus_type_choice, label="", initial='', widget=forms.Select(), required=True)
    bus_model=forms.ChoiceField(choices = bus_model_choice, label="", initial='', widget=forms.Select(), required=True)
    costperkm=forms.FloatField(required=True,widget=forms.TextInput())
    serviceno=forms.CharField(min_length=1,max_length=100,required=True,widget=forms.TextInput())
    noseats=forms.IntegerField(required=True,widget=forms.TextInput())
    start_city=forms.CharField(min_length=1,max_length=100,required=True,widget=forms.TextInput())
    destination_city=forms.CharField(min_length=1,max_length=100,required=True,widget=forms.TextInput())
    startdate=forms.DateField()
    start_time=forms.IntegerField(required=True,widget=forms.TextInput())
    reach_time=forms.IntegerField(required=True,widget=forms.TextInput())
    reachdate=forms.DateField()


    class Meta:
        model = Bus
        fields = ['bus_type','bus_model','costperkm','serviceno','noseats','start_city','destination_city','startdate','start_time','reach_time','reachdate']

class via(forms.Form):
    place_name=forms.CharField()
    reach_date=forms.DateField()
    reach_time=forms.IntegerField(required=True,widget=forms.TextInput())
    start_date=forms.DateField()
    start_time=forms.IntegerField(required=True,widget=forms.TextInput())
    distance_from_startcity=forms.FloatField()

    class Meta:
        model = via
        fields = ['place_name','reach_date','reach_time','start_date','start_time','distance_from_startcity']
