from django.urls import path, include
from . import views


app_name = 'point_workshop'


urlpatterns = [
    path('', views.home, name='home'),
    
]