from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


# Create your views here.

# class Home(LoginRequiredMixin, generic.TemplateView):
#     template_name = "index.html"

@login_required
def home(request):
    # print(request.user.roles.all())
    return render(request, 'ar/index.html')


