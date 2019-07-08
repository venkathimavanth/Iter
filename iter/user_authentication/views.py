
from django.shortcuts import render,redirect
from user_authentication.forms import UserRegisterForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.urls import reverse
from user_authentication.models import Profile
from .forms import UserRegisterForm, EditProfileForm, UserProfileForm
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage, send_mail
from django.contrib.auth import update_session_auth_hash
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm , PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from bus_booking.models import Bus_agency
from hotel_booking.models import Hotels


# Create your views here.

def home(request):
    # Create your views here.

    return render(request, "user_authentication/homepage.html")


def signup(request):
    # Create your views here.
    if request.method=='POST':

        form=UserRegisterForm(request.POST,request.FILES)
        if form.is_valid():

            username=form.cleaned_data.get('username')
            raw_password=form.cleaned_data.get('password1')
            new_user = form.save(commit=False)
            new_user.is_active=False
            new_user.save()
            new_user.refresh_from_db()  # load the profile instance created by the signal
            new_user.save()
            phone_number = form.cleaned_data.get('phone_number')
            picture = form.cleaned_data.get('picture')
            profile=Profile()
            profile.user = new_user
            profile.phone_number = phone_number
            profile.user_type='C'
            if picture:
                profile.picture = picture
            profile.save()

            current_site = get_current_site(request)
            mail_subject = 'Activate your Iter account.'
            message = render_to_string('user_authentication/acc_active_email.html', {
                'user': new_user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(new_user.pk)),
                'token':account_activation_token.make_token(new_user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')


        print(form)
    else:
        form = UserRegisterForm()
        print(form)

    return render(request, "user_authentication/signuppage.html",{'form':form})

def bussignup(request):
    # Create your views here.
    if request.method=='POST':

        form=UserRegisterForm(request.POST,request.FILES)
        if form.is_valid():

            username=form.cleaned_data.get('username')
            raw_password=form.cleaned_data.get('password1')
            new_user = form.save(commit=False)
            new_user.is_active=False
            new_user.save()
            new_user.refresh_from_db()  # load the profile instance created by the signal
            new_user.save()
            phone_number = form.cleaned_data.get('phone_number')
            picture = form.cleaned_data.get('picture')
            profile=Profile()
            profile.user = new_user
            profile.phone_number = phone_number
            profile.user_type='B'
            if picture:
                profile.picture = picture
            profile.save()

            current_site = get_current_site(request)
            mail_subject = 'Activate your Iter account.'
            message = render_to_string('user_authentication/acc_active_email.html', {
                'user': new_user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(new_user.pk)),
                'token':account_activation_token.make_token(new_user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')


        print(form)
    else:
        form = UserRegisterForm()
        print(form)

    return render(request, "user_authentication/signuppage.html",{'form':form})

def hotelsignup(request):
    # Create your views here.
    if request.method=='POST':

        form=UserRegisterForm(request.POST,request.FILES)
        if form.is_valid():

            username=form.cleaned_data.get('username')
            raw_password=form.cleaned_data.get('password1')
            new_user = form.save(commit=False)
            new_user.is_active=False
            new_user.save()
            new_user.refresh_from_db()  # load the profile instance created by the signal
            new_user.save()
            phone_number = form.cleaned_data.get('phone_number')
            picture = form.cleaned_data.get('picture')
            profile=Profile()
            profile.user = new_user
            profile.phone_number = phone_number
            profile.user_type='H'
            if picture:
                profile.picture = picture
            profile.save()

            current_site = get_current_site(request)
            mail_subject = 'Activate your Iter account.'
            message = render_to_string('user_authentication/acc_active_email.html', {
                'user': new_user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(new_user.pk)),
                'token':account_activation_token.make_token(new_user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')


        print(form)
    else:
        form = UserRegisterForm()
        print(form)

    return render(request, "user_authentication/signuppage.html",{'form':form})


def user_login(request):
    if request.method == 'POST':
        form=AuthenticationForm(request.POST)
        uname = request.POST.get('username')
        password = request.POST.get('password')
        print(request.POST)
        admin = authenticate(username=uname, password=password)

        if admin:
            x = Profile.objects.get(user=admin)
            if admin.is_active and x.user_type == 'H':
                login(request,admin)
                if Hotels.objects.filter(user=request.user):
                    return HttpResponseRedirect("/hotel_vendor/home")
                else:
                    return HttpResponseRedirect("/hotel_vendor/add_hotel")

                #return HttpResponseRedirect(reverse('hotel_vendor:home'))
                return HttpResponseRedirect('hotel_vendor:hotels')
            elif admin.is_active and x.user_type == 'C':
                login(request,admin)

                #return HttpResponseRedirect(reverse('cus_login:home'))
                #return render(request, 'user_authentication/home.html')

                return redirect('bus_booking:buses')
            elif admin.is_active and x.user_type == 'B':
                login(request,admin)
                #return HttpResponseRedirect(reverse('cus_login:home'))
                #return HttpResponseRedirect(reverse('hotel_vendor:home'))
                if Bus_agency.objects.filter(user=request.user):
                    return HttpResponseRedirect("/bus_vendor/buses")
                else:
                    return HttpResponseRedirect("/bus_vendor")
            else:
                return HttpResponse("Account has been diasabled!")
        else:
            print('x')
            return render(request, 'user_authentication/loginpage.html', {'err':'Invalid Login Details!','form':form})
    form=AuthenticationForm()
    print(form)
    return render(request, 'user_authentication/loginpage.html',{'form':form})

@login_required
def logoutuser(request):
    logout(request)
    return HttpResponseRedirect(reverse('user_authentication:user_login'))


def edit_profile(request):
    if request.method == 'POST':
        passform = PasswordChangeForm(request.user, request.POST)
        user_form = EditProfileForm(request.POST,instance=request.user)
        print(user_form)
        profile_form = UserProfileForm(request.POST, request.FILES,instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            print(user_form)
            user_form.save()
            profile_form.save()
            messages.success(request, ('Your profile was successfully updated!'))
            return redirect('user_authentication:edit_profile')
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        print('outside')
        user_form = EditProfileForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.profile)
        passform = PasswordChangeForm(request.user, request.POST)

    return render(request, 'user_authentication/profile_edit.html', {
            'user_form': user_form,
            'profile_form': profile_form,
            'passform':passform,
            'user':request.user
        })

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('user_authentication.view_profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'user_authentication/change_password.html', {
        'form': form
    })

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed=True
        user.save()
        user.profile.save()

        login(request, user)
        if request.user.profile.user_type=='C':
            return redirect(reverse('bus_booking:buses'))
        if request.user.profile.user_type=='B':
            return redirect(reverse('bus_vendor:list_agency'))
        if request.user.profile.user_type=='H':
            return redirect(reverse('hotel_vendor:add_hotel'))

    else:
        return HttpResponse('Activation link is invalid!')
