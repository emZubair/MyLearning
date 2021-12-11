from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from .forms import LoginForm, EmailSendingForm


def login_user(request):
    import pdb
    # pdb.set_trace()
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
