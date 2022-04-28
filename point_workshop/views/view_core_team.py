from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from ..decorators import user_assigned_role_decorator




decorators = [login_required, user_assigned_role_decorator]

# @method_decorator(decorators, name='dispatch')
class Home(generic.TemplateView):
    template_name = "point_workshop/core-team/index.html"