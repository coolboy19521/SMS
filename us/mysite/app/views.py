from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .models import Museum, Exhibit

def us(request):
    return render(request, 'us.html')

def home(request):
    return render(request, 'home.html')

def exhibit(request, id):
    print(id)
    context = {
        'exhibit' : Exhibit.objects.get(id = int(id))
    }

    #Exhibit.audio.url = Exhibit.audio.url[Exhibit.audio.url.index('/') + 1: ]
    #Exhibit.video.url = Exhibit.video.url[Exhibit.video.url.index('/') + 1: ]
    #Exhibit.thumbnail.url = Exhibit.thumbnail.url[Exhibit.thumbnail.url.index('/') + 1 : ]

    return render(request, 'exhibit.html', context)

def museums(request):
    context = {
        'exhibits' : Exhibit.objects.all()
    }
    """
    for exhibit in context['exhibits']:
        Exhibit.audio.url = Exhibit.audio.url[Exhibit.audio.url.index('/') + 1: ]
        Exhibit.video.url = Exhibit.video.url[Exhibit.video.url.index('/') + 1: ]
        Exhibit.thumbnail.url = Exhibit.thumbnail.url[Exhibit.thumbnail.url.index('/') + 1 : ]
    """
    if request.method == 'POST':
        museum_key = request.POST.get('key')[::-1]
        museum_key = museum_key[museum_key.index('b') + 1 :][::-1]
        museum = Museum.objects.filter(key = museum_key).first()
        exhibit = Exhibit(
            museum = museum,
            name = request.POST.get('name'),
            audio = request.FILES['audio'],
            video = request.FILES['video'],
            thumbnail = request.FILES['thumb'],
            desc = request.POST.get('desc')
        )

        exhibit.save()

        print(exhibit.id)
        context['url'] = request.session.get('url')
        request.session['url'] = f'https://enca.pythonanywhere.com/exhibit/{exhibit.id}'

        return redirect('museums')

    context['url'] = request.session.get('url')

    return render(request, 'museums.html', context)

def add_museum(request):
    if request.user.is_authenticated and request.method == 'POST':
        Museum(
            name = request.POST.get('name'),
            address = request.POST.get('address'),
            key = request.POST.get('key'),
        ).save()

    return redirect('admin_museums')

def edit_museum(request):
    if request.user.is_authenticated and request.method == 'POST':
        museum = Museum.objects.get(id = int(request.POST.get('id')))
        museum.name = request.POST.get('name')
        museum.address = request.POST.get('address')
        museum.key = request.POST.get('key')
        museum.save()

    return redirect('admin_museums')

def delete_museum(request):
    if request.user.is_authenticated and request.method == 'POST':
        Museum.objects.get(id = int(request.POST.get('id'))).delete()

    return redirect('admin_museums')

def admin_museums(request):
    if request.user.is_authenticated:
        context = {
            'museums' : Museum.objects.all(),
        }

        return render(request, 'admin_museums.html', context)
    else:
        return redirect('admin_login')

def admin_login(request):
    if request.method == 'POST':
        user = authenticate(request, username = request.POST.get('username'), password = request.POST.get('password'))

        if user:
            login(request, user)

            return redirect('admin_museums')

    return render(request, 'admin_login.html')

def logout_view(request):
    logout(request)

    return redirect('home')
