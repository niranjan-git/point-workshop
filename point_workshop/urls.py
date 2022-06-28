from django.urls import path, include
from .views import view_common, view_core_team, view_ar, view_zone


app_name = 'point_workshop'


urlpatterns = [
    path('', view_common.Home.as_view(), name='home'),

    path('ar/', view_ar.Home.as_view(), name='ar-home'),





    path('zone/', view_zone.Home.as_view(), name='zone-home'),



    
    path('core-team/', view_core_team.Home.as_view(), name='core-team-home'),
    path('core-team/user-list/', view_core_team.user_list, name='user-list'),
    
]