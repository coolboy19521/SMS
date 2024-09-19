from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .models import Museum, Exhibit

def us(request):
    return render(request, 'us.html')

def home(request):
    return render(request, 'home.html')

def project(request):
    return render(request, 'project.html')