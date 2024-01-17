from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect

from rest_framework.decorators import api_view
from rest_framework.response import Response
from uuid import uuid4

from .models import *

@api_view(['POST'])
def addAnEmployee(request):
    pasd = uuid4().hex[: 8]

    Employee(
        name = request.POST['name'],
        sidd = request.POST['sidd'],
        pasd = pasd
    ).save()

    return Response({'pasd' : pasd})

@api_view(['POST'])
def adminLogIn(request):
    user = authenticate(username = request.POST.get('user'), password = request.POST.get('pasd'))

    if user:
        print('hey')
        login(request, user)

        return redirect('home')

    return Response('FUCK')

@api_view(['POST'])
def logOut(request):
    if request.user.is_authenticated:
        logout(request)

        return redirect('login')

    return Response('FUCK')