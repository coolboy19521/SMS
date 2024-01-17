from django.shortcuts import render, redirect

def login(request):
    if request.user.is_authenticated:
        return redirect('home')

    return render(request, 'login.html')

def home(request):
    return render(request, 'home.html')