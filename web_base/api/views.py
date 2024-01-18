from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.db.models import Q

from rest_framework.decorators import api_view
from rest_framework.response import Response
from uuid import uuid4

from .serializers import *
from .models import *

@api_view(['POST'])
def addADevice(request):
    pasd = uuid4().hex[: 8]

    Device(
        nump = request.POST['nump'],
        pasd = make_password(pasd),
        urln = f"/devices/{request.POST['nump']}",
        firs = True
    ).save()

    return Response({'pasd' : pasd})

@api_view(['POST'])
def adminLogIn(request):
    user = authenticate(username = request.POST.get('user'), password = request.POST.get('pasd'))

    if user:
        login(request, user)

        return redirect('robots')

    return Response('FUCK')

@api_view(['POST'])
def deviceLogIn(request):
    print(request.POST.get('nump'))
    device = Device.objects.get(nump = request.POST.get('nump'))

    if device:
        pasd = device.pasd

        if check_password(request.POST.get('pasd'), pasd):
            request.session['deviceLoggedIn'] = True
            request.session['deviceId'] = device.id

            return redirect('deviceHome')

    return Response('FUCK')

@api_view(['POST'])
def logOut(request):
    if request.user.is_authenticated:
        logout(request)

        return redirect('login')

    return Response('FUCK')

@api_view(['GET'])
def getAllDevices(request):
    serializer = DeviceSerializer(Device.objects.all(), many = True)

    return Response(serializer.data)

@api_view(['GET'])
def getADevice(request):
    searchText = request.GET.get('searchText')

    print(searchText)

    devices = Device.objects.filter(Q(nump__icontains = searchText) | Q(date__icontains = searchText) | Q(time__icontains = searchText))

    for device in devices:
        device.url = '347239'

    serializer = DeviceSerializer(devices, many = True)

    return Response(serializer.data)

@api_view(['GET'])
def getSpecificDevice(request, q):
    device = Device.objects.get(nump = q)
    serializer = DeviceSerializer(device, many = False)

    return Response(serializer.data)