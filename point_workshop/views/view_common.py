from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from ..decorators import user_assigned_role_decorator
from ..import models


# Create your views here.

decorators = [login_required, user_assigned_role_decorator]


def get_user_role(request):
    role_list = []
    try:
        print("User: ",request.user)
        user_role = models.UserAssignedRole.objects.get(user=request.user)
        print("User role: ",user_role.role)
        if user_role is not None:
            uid = user_role.role.id
            if uid == 2:
                role_list.append("branch")
                role_list.append(user_role.branch.id)
            if uid == 5:
                role_list.append("branch")
                role_list.append(user_role.branch.id)
    except Exception as e:
        print("Exception at view_common get_user_role method: ",e)

    return role_list


@method_decorator(decorators, name='dispatch')
class Home(LoginRequiredMixin, generic.TemplateView):
    template_name = "point_workshop/index.html"


@login_required
def user_list(request):
    # print(request.user.roles.all())
    role_list = get_user_role(request)
    
    print("role_list: ",role_list)
    kwargs = {
        '{0}'.format(role_list[0]) : role_list[1]
        
    }
    users = models.UserAssignedRole.objects.filter(**kwargs)
    context = {
        'users' : users 
    }

    print("users: ",users)
    return render(request, 'point_workshop/core-team/user_list.html',context)
