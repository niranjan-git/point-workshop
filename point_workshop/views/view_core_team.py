from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from ..decorators import user_assigned_role_decorator, core_team_decorator
from ..import models

try:
    from user.models import User
except:
    pass




decorators = [login_required, core_team_decorator]

@method_decorator(decorators, name='dispatch')
class Home(generic.TemplateView):
    template_name = "point_workshop/core-team/index.html"



@login_required
@core_team_decorator
def user_list(request):
    # print(request.user.roles.all())
    users = models.UserAssignedRole.objects.core()
    context = {
        'users' : users 
    }

    print("users: ",users)
    return render(request, 'point_workshop/core-team/user_list.html',context)
