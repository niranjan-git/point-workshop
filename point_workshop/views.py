from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

# class Home(LoginRequiredMixin, generic.TemplateView):
#     template_name = "index.html"


def home(request):
    print(request.user.roles.all())
    return render(request, 'index.html')


