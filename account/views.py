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
from .auth_backend import backend
from ratelimit import limits
# Create your views here.

def register(request):
    registered = False
    phone = request.session['phone']
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():

            user = form.save(commit=False)
            user.set_password(user.password)
            user.phone = request.POST['phone']
            request.session['password'] = user.password
            request.session['name'] = request.POST['name']
            request.session['last_name'] = request.POST['last_name']
            return redirect('verify')

    return render(request,'account/Register.html',context={'form1':form,'phone':phone})

@limits(calls = 3, period=3600)
def user_login(request):
    lform = LoginForm()
    session_phone = request.session['phone']
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
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, 'account/login2.html', context={'form':lform} )

def index(request):
    if request.method == 'POST':
        request.session['phone'] = request.POST['phone']
        phone = request.POST['phone']

        if User.objects.filter(phone=phone):
            return redirect('login')
        else:
            return redirect('register')

    return render(request,'account/index.html')

@limits(calls = 3, period=3600)
@is_registered
def verify(request):

    phone = request.session.get('phone')
    password = request.session.get('password')
    user = User(phone=phone,password=password)
    user.is_active =True
    user.set_password(user.password)
    user.name = request.session['name']
    user.last_name = request.session['last_name']
    # print(User.objects.get(phone=phone))
    api = KavenegarAPI('4B4B49434E56576475475A67387A6D61426150486F4D584E306B686469497A6176672F7644563651536A303D')
    #TODO actually buy the full servis in order to send sms to all users not just yourself!
    key = randint(100000,999999)
    # I dont have enough account charge left in my kavenegar account so the there will be no sms sent
    try:
        api = KavenegarAPI('Your APIKey')
        params = {'sender': '1000596446', 'receptor': '09190357713', 'message': 'Verification Code : {}'.format(key)}
        response = api.sms_send(params)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)
    if request.method == 'POST':

        user_key = request.POST['Verification']

        if user_key == key:
            user.save()
            return redirect(index)

    return render(request,'account/phone_verify.html')

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
