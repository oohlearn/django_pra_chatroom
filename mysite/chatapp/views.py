from django.shortcuts import render, redirect
from .models import Room, ChatMessage
from .forms import LoginForm
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout



# Create your views here.
def index(request):
    rooms = Room.objects.all()
    form = LoginForm(request)
    return render(request, 'chatapp/index.html', {
        'rooms': rooms,
        "form": form,
    })


def detail(request, slug):
    room = Room.objects.get(slug=slug)
    chat_message = ChatMessage.objects.filter(room=room)[0:30]
    return render(request, 'chatapp/detail.html',
                  {'room': room,
                   "chat_message": chat_message})


def user_login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request,
                                username=data['username'],
                                password=data['password'])
            if user is not None:
                login(request, user)
                return redirect('/rooms')
    return render(request, 'chatapp/user_login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect("rooms/")
