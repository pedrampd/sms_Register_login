from django.shortcuts import render,redirect
from .forms import RegisterForm,LoginForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .decorators import is_registered
from .models import User
from kavenegar import *
from random import randint
from django.contrib.auth.decorators import login_required
# Create your views here.
def register(request):
    registered = False

    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            # TODO send an sms to confirm

            user = form.save(commit=False)
            user.set_password(user.password)
            request.session['phone'] = user.phone
            request.session['password'] = user.password
            return redirect('verify')

    return render(request,'account/Register.html',context={'form1':form})

def user_login(request):
    lform = LoginForm()
    if request.method == 'POST':
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        lform = LoginForm(data=request.POST)
        user = User(phone=phone,password=password)
        user.set_password(password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used phone number : {} and password: {}".format(phone,password))
            return HttpResponse("Invalid login details supplied.")

    else:
        #Nothing has been provided for username or password.
        return render(request, 'account/login2.html', context={'form':lform})

def index(request):
    return render(request,'account/index.html')

@is_registered
def verify(request):
    phone = request.session.get('phone')
    password = request.session.get('password')
    user = User(phone=phone,password=password)
    api = KavenegarAPI('4B4B49434E56576475475A67387A6D61426150486F4D584E306B686469497A6176672F7644563651536A303D')
    #TODO actually buy the full servis in order to send sms to all users not just yourself!
    key = randint(100000,999999)
    params = {'sender': '1000596446', 'receptor': '09190357713', 'message': 'Verification Code : {}'.format(key)}
    response = api.sms_send(params)
    if request.method == 'POST':
        user_key = request.POST['Verification']
        print(user_key)
        if user_key == key:
            user.save()
            return redirect(index)

        else:
            pass
    return render(request,'account/phone_verify.html')
# @register
# def verify(request):

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
