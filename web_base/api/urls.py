from django.urls import path
from .views import *

urlpatterns = [
    path('addAnEmployee', addAnEmployee),
    path('adminLogIn', adminLogIn),
    path('logOut', logOut)
]