from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    data={"content": "Ласкаво просимо на головну сторінку"}
    return render(request, 'home.html', data)

def about(request):
    data={"content": "Сторінка про нас"}
    return render(request, "about.html", data)

def contact(request):
    data = {"content": "Зв'яжіться з нами"}
    return render(request, "contact.html", data)

def post_view(request, id):
    data = {"content": f"Ви переглядаєте пост з ID: {id}"}
    return render(request, "post.html", data)

def profile_view(request, username):
    data = {"content": f"Ви переглядаєте пост з ID: {username}"}
    return render(request, "profile.html", data)

def event_view(request, year, month, day):
    data = {"content": f"Дата події: {year}-{month}-{day}."}
    return render(request, "event.html", data)
# Create your views here.
