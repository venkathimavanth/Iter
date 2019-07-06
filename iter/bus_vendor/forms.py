from django import forms
from bus_booking.models  import Bus_agency,Bus,via

class agency_details(forms.ModelForm):

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
        ('Semi Sleeper', 'Semi Sleeper'),
        ('Seater', 'Seater'),



                            )
    bus_model_choice = (
        ('scania','scania'),
        ('volvo', 'volvo'),
        ('super luxary', 'super luxary'),

        ('Normal', 'Normal'),

                            )
    bus_type=forms.ChoiceField(choices = bus_type_choice, label="", initial='', widget=forms.Select(), required=True)
    bus_model=forms.ChoiceField(choices = bus_model_choice, label="", initial='', widget=forms.Select(), required=True)
    costperkm=forms.FloatField(required=True,widget=forms.TextInput())
    serviceno=forms.CharField(min_length=1,max_length=100,required=True,widget=forms.TextInput())
    noseats=forms.IntegerField(required=True,widget=forms.TextInput())
    start_city=forms.CharField(min_length=1,max_length=100,required=True,widget=forms.TextInput())
    destination_city=forms.CharField(min_length=1,max_length=100,required=True,widget=forms.TextInput())
    start=forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M'],widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        }))
    reach=forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M'],widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker2'
        }))

    class Meta:
        model = Bus
        fields = ['bus_type','bus_model','costperkm','serviceno','noseats','start_city','destination_city','start','reach']

class via_details(forms.Form):
    serviceno=forms.CharField()
    place_name=forms.CharField()
    reach=forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M'])

    distance_from_startcity=forms.FloatField()

    class Meta:
        model = via
        fields = ['place_name','reach','serviceno','distance_from_startcity']

class date_test(forms.Form):
    monday = forms.BooleanField( widget=forms.CheckboxInput())
    tuesday = forms.BooleanField( widget=forms.CheckboxInput())
    wednesday = forms.BooleanField( widget=forms.CheckboxInput())
    thursday = forms.BooleanField( widget=forms.CheckboxInput())
    friday = forms.BooleanField( widget=forms.CheckboxInput())
    saturday = forms.BooleanField( widget=forms.CheckboxInput())
    sunday = forms.BooleanField( widget=forms.CheckboxInput())

class dateform(forms.Form):
    date=forms.DateField(input_formats=['%Y-%m-%d'])
