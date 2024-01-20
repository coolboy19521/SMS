from django.views.generic.base import RedirectView
from django.shortcuts import render, redirect

def login(request):
    if request.user.is_authenticated:
        return redirect('robots')

    return render(request, 'login.html')

def robots(request):
    if request.user.is_authenticated:
        return render(request, 'robots.html')

    return redirect('login')

def devices(request):
    if request.user.is_authenticated:
        return render(request, 'devices.html')

    return redirect('login')

def device(request, q):
    if request.user.is_authenticated:
        return render(request, 'device.html', {
            'device' : q
        })

    return redirect('login')

def deviceHome(request):
    if request.session.get('deviceLoggedIn', False):
        print('hey')

        return render(request, 'deviceHome.html', {
            'deviceId': request.session['deviceId'],
            'firs': request.session['firs']
        })

    return redirect('login')

favicon = RedirectView.as_view(url='/static/favicon.ico', permanent=True)