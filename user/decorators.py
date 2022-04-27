from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse


def email_session_required(function):
    def wrap(request, *args, **kwargs):
        if request.session.has_key('email'):
            return function(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/')
    # wrap.__doc__ = function.__doc__
    # wrap.__name__ = function.__name__
    return wrap



def otp_session_required(function):
    def wrap(request, *args, **kwargs):
        if request.session.has_key('otp'):
            return function(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/')
    return wrap


def destroy_session(function):
    def wrap(request, *args, **kwargs):
        try:
            if request.session.session_key:
                request.session.flush()
                return function(request, *args, **kwargs)
            else:
                return function(request, *args, **kwargs)
        except Exception as e:
            pass
    return wrap
