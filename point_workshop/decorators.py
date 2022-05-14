from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from .models import UserAssignedRole



def user_assigned_role_decorator(function):
    def wrap(request, *args, **kwargs):
        try:
            print("User: ",request.user)
            user_role = UserAssignedRole.objects.get(user=request.user)
            # print("User role: ",user_role.role)
            if user_role is not None:
                uid = user_role.role.id
                if uid == 2:
                    return redirect("point_workshop:ar-home")
                elif uid == 5:
                    return redirect("point_workshop:core-team-home")
                else:
                    print("user role is: ",user_role.role)
                    return redirect("user:logout")
            else:
                print("No any role is assigned to User ",request.user)
            return function(request, *args, **kwargs)
        except Exception as e:
            print("Exception at user_assigned_role_decorator: ",e)
            return function(request, *args, **kwargs)
    return wrap



def core_team_decorator(function):
    def wrap(request, *args, **kwargs):
        try:
            print("User: ",request.user)
            user_role = UserAssignedRole.objects.get(user=request.user)
            print("User role: ",user_role.role)
            if user_role is not None:
                uid = user_role.role.id
                if uid == 5:
                    return function(request, *args, **kwargs)
                else:
                    return redirect("user:login")
            else:
                print("No any role is assigned to User ",request.user)
            return redirect("user:login")
        except Exception as e:
            print("Exception at core_team_decorator: ",e)
            return redirect("user:login")
    return wrap


def ar_decorator(function):
    def wrap(request, *args, **kwargs):
        try:
            print("User: ",request.user)
            user_role = UserAssignedRole.objects.get(user=request.user)
            print("User role: ",user_role.role)
            if user_role is not None:
                uid = user_role.role.id
                if uid == 2:
                    return function(request, *args, **kwargs)
                else:
                    return redirect("user:login")
            else:
                print("No any role is assigned to User ",request.user)
            return redirect("user:login")
        except Exception as e:
            print("Exception at ar_decorator: ",e)
            return redirect("user:login")
    return wrap

