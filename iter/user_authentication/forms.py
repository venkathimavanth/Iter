from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from user_authentication.models import Profile




class UserRegisterForm(UserCreationForm):

    phone_number=forms.CharField(min_length=10,max_length=10,required=True,widget=forms.TextInput())
    picture=forms.ImageField( required=False, )
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    class Meta:
        model = User
        fields = ['username', 'email','first_name','last_name', 'password1', 'password2']


class UserProfileForm(forms.ModelForm):



    class Meta:
        model=Profile
        fields=['phone_number','picture' ]


    def save(self, user=None):
        user_profile=super(UserProfileForm, self).save(commit=False)
        if user:
            user_profile.user=user
        user_profile.save()
        return user_profile


class EditProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name','last_name']
