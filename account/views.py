from django.shortcuts import render, redirect
from .forms import (
    LoginForm, 
    PsswordChangeForm, 
    PsswordResetRequestForm,
    SetNewPasswordForm,
    UserRegistrasionForm
)
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
#from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


# Create your views here.


def user_registrasion(request):
    if request.method == 'POST':
        form = UserRegistrasionForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(
                form.cleaned_data['password']
            )
            new_user.save()
            messages.success(request,f'{new_user.username} succesfully register your new account\n login now')
            return redirect ('login')
    else:
        form = UserRegistrasionForm()
    return render (request,'account/user_registrasion.html',
                   {
                       'form':form
                   })

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request,
                username = cd['username'],
                password = cd['password']
            )
            if user is not None:
                if user.is_active:
                    login(request,user)
                    next_url = request.GET.get('next')
                    if next_url:
                        return redirect (next_url)
                    return redirect ('dashboard')
                else:
                    messages.error(request,'user is not active')
            else:
                messages.error(request,'user not found')

    else:
        form = LoginForm()
    return render (request,'account/login.html',
                   {'form':form})

@login_required
def user_logout(request):
    logout(request)
    messages.success(request,'succesfully logout')
    return redirect('login')

@login_required
def dashboard(request):
    return render (request,'account/dashboard.html',{
        'section':'dashboard'
    })

@login_required
def password_change(request):
    if request.method == 'POST':
        form = PsswordChangeForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)

            messages.success(request,'succesfully chenge your pssword')
            return redirect ('dashboard')

    else:
        form = PsswordChangeForm()
    return render (request, 'account/password_change.html',
                   {'form':form})



def password_reset_request(request):
    if request.method == 'POST':
        form = PsswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            domain = request.get_host()
            reset_link = f'http://{domain}/account/password_reset_confirm/{uid}/{token}'
            subject = 'password reset request'
            message = f'{user.username} clickh this link and reset your password\n {reset_link}'
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [email]
            )
            messages.success(request,'check you email and reset your password')
            return redirect('password_reset_request')

    else:
        form = PsswordResetRequestForm()
    return render (request,'account/password_reset_request.html',
                   {
                        'form':form
                   })

def password_reset_confirm(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetNewPasswordForm(request.POST)
            if form.is_valid():
                new_password = form.cleaned_data['new_password']
                user.set_password(new_password)
                user.save()

                messages.success(request,'succesfully chenge your password')
                return redirect ('login')
        else:
            form = SetNewPasswordForm()
        return render (request,'account/password_reset_confirm.html',
                       {
                           'form':form
                       })
    else:
        messages.error(request, 'this link is no valid')
        return redirect ('password_reset_request')
