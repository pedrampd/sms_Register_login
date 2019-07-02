from django.shortcuts import render
from .forms import RegisterForm,LoginForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .models import User
from django.contrib.auth.decorators import login_required
# Create your views here.
def register(request):
    registered = False

    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            # TODO send an sms to confirm
            user = form.save()
            user.set_password(user.password)
            user.save()
            registered = True
    return render(request,'account/Register.html',context={'form1':form})


def user_login(request):
    lform = LoginForm()
    if request.method == 'POST':
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        lform = LoginForm(data=request.POST)
        user = authenticate(request,phone=phone,password=password)
        #user = authenticate(phone=phone, password=password)
        user = User(phone=phone,password=password)
        user.set_password(password)
        print(type(user))
        print(user)
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
