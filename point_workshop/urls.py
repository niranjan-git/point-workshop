from django.urls import path, include
from .views import common


app_name = 'point_workshop'


urlpatterns = [
    path('', common.Home.as_view(), name='home'),
    
]