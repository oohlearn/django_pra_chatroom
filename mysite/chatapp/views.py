from django.shortcuts import render
from .models import Room


# Create your views here.
def index(request):
    rooms = Room.objects.all()
    return render(request, 'chatapp/index.html', {
        'rooms': rooms,
    })


def detail(request, slug):
    room = Room.objects.get(slug=slug)
    return render(request, 'chatapp/detail.html', {'room': room})
