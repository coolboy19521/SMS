from django.urls import path
from .views import *

urlpatterns = [
    path('addADevice', addADevice),
    path('adminLogIn', adminLogIn),
    path('deviceLogIn', deviceLogIn),
    path('logOut', logOut),
    path('getAllDevices', getAllDevices),
    path('getADevice', getADevice),
    path('getSpecificDevice/<str:q>', getSpecificDevice),
    path('updateDeviceGPS/<int:id>', updateDeviceGPS),
    path('changeDevicePassword/<int:id>', changeDevicePassword),
    path('deviceLogOut', deviceLogOut),
    path('updateDevicePlatform/<int:id>', updateDevicePlatform),
    path('deviceDelete/<int:id>', deviceDelete),
    path('addARobot', addARobot),
    path('updatePercFpsf', updatePercFpsf),
    path('getARobot', getARobot),
    path('updateLatiLongF1F2', updateLatiLongF1F2),
    path('getAllRobots', getAllRobots)
]