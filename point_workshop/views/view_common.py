from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from ..decorators import user_assigned_role_decorator


# Create your views here.

decorators = [login_required, user_assigned_role_decorator]


@method_decorator(decorators, name='dispatch')
class Home(LoginRequiredMixin, generic.TemplateView):
    template_name = "point_workshop/index.html"


# @method_decorator(decorators, name='dispatch')
# def home(request):
#     # print(request.user.roles.all())
#     return render(request, 'point_workshop/ar/index.html')


