from django.shortcuts import render
from basicApp.forms import UserForm,UserProfileInfoForm

#
from django.contrib.auth import authenticate,logout,login
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
    return render(request,'basicApp/index.html')

@login_required
def user_logout(request):
    # Log out user
    logout(request)
    # Return to Homepage
    return HttpResponseRedirect(reverse('index'))

def register(request):
    registered=False

    if request.method=='POST':
        user_form=UserForm(data=request.POST)
        profile_form=UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user=user_form.save()
            user.set_password(user.password)
            user.save()

            profile=profile_form.save(commit=False)
            profile.user=user
            if 'profile_pic' in request.FILES:
                profile.profile_pic=request.FILES['profile_pic']
            profile.save()
            registered=True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form=UserForm()
        profile_form=UserProfileInfoForm()
    return render(request,'basicApp/registration.html',{'user_form':user_form,
                                                        'profile_form':profile_form,
                                                        'registered':registered})
def user_login(request):
    if request.method=='POST':
        print('dsda')
        username=request.POST.get('username')
        password=request.POST.get('password')

        # inbuilt authentication function
        user=authenticate(username=username,password=password)

        # if user authenticated
        if user:
            if user.is_active:
                # log the user if
                login(request,user)
                # redirect user after login
                return HttpResponseRedirect(reverse('index'))
            else:
                # if account not not active:
                return HttpResponse('your account is not active')
        else:
            print('someone tried login and failed')
            print('Used username: {} and password: {}'.format(username,password))
            return HttpResponse('Invalid Credentials')
    else:
        # nothing yes provided in username and password field
        return render(request,'basicApp/login.html',{})
