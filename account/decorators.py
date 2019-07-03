from functools import wraps
from django.http import HttpResponseRedirect
from .models import User

from django.urls import reverse

def is_registered(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        print("hello")
        phone = request.session.get('phone')
        if phone:
             return function(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('index'))
    return wrap