from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required



class Home(LoginRequiredMixin, generic.TemplateView):
    template_name = "point_workshop/ar/index.html"