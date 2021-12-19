from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from .models import Profile
from .forms import (LoginForm, EmailSendingForm, UserRegistrationForm,
                    UserEditForm, ProfileEditForm)


def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            user = authenticate(request, username=cleaned_data.get('username'),
                                password=cleaned_data.get('password'))
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated Successfully')
                else:
                    return HttpResponse('Inactive User')
            else:
                return HttpResponse('Invalid credentials')
    else:
        form = LoginForm()

    return render(request, 'account/login.html', {
        'form': form, 'is_login': 'login' in request.get_full_path()
    })


@login_required
def dashboard(request):
    if request.method == 'POST':
        print("sending Email")
        send_mail("Welcome to Django", "This email was sent using a silly Form",
                  from_email='testingbyzeedo@gmail.com',
                  recipient_list=['zubair1714@gmail.com'])

    return render(request, 'account/dashboard.html',
                  {'section': 'dashboard', 'form': EmailSendingForm()})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data.get('password'))
            new_user.save()
            Profile.objects.save(user=new_user)
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


@login_required
def edit_user(request):
    current_user = request.user
    if request.method == 'POST':
        user_form = UserEditForm(instance=current_user, data=request.POST)
        profile_form = ProfileEditForm(instance=current_user.profile, data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile Updated Successfully')
        else:
            messages.error(request, 'Failed to update the profile')
    else:
        user_form = UserEditForm(instance=current_user)
        profile_form = ProfileEditForm(instance=current_user.profile)

    return render(request, 'account/edit.html',
                  {'user_form': user_form, 'profile_form': profile_form})
