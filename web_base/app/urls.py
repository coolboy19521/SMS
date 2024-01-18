from django.urls import path
from .views import *


urlpatterns = [
    path('', login, name = 'login'),
    path('robots', robots, name = 'robots'),
    path('devices', devices, name = 'devices'),
    path('devices/<str:q>', device),
    path('deviceHome', deviceHome, name = 'deviceHome'),
    path('favicon.ico', favicon)
]