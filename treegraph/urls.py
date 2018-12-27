from django.urls import path

from .views import *

urlpatterns = [
    path('',  nodes_list),
    path('time_settings_<int:Nodes_id>/', detail, name='detail'),
    path('graph/', graph),
]