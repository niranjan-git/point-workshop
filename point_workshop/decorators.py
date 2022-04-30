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
            print("User role: ",user_role.role)
            if user_role is not None:
                uid = user_role.role.id
                if uid == 1:
                    return redirect("point_workshop:core-team-home")
                elif uid == 2:
                    return redirect("point_workshop:core-team-home")
            else:
                print("No any role is assigned to User ",request.user)
            return function(request, *args, **kwargs)
        except Exception as e:
            print("Exception at user_assigned_role_decorator: ",e)
            return function(request, *args, **kwargs)
    return wrap