import redis
from celery.result import AsyncResult
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import login, authenticate, logout as django_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django_ratelimit.decorators import ratelimit
from typing import Any
from cryptography.fernet import Fernet
import os

from app.forms import SignUpForm, LogInForm, ProfileForm, EditProfileForm, ServerCreateForm, ServerEditForm
from app.models import MonUser, Profile, Server
from celery_tasks.tasks import server_stats, active_monitoring_tasks

fernet = Fernet(os.getenv("ENCRYPTION_KEY").encode())


@ratelimit(key='ip', rate='100/m', method='GET', block=True)
def signup(request: Any) -> HttpResponse:
    form = SignUpForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data["password"])
        user.save()
        login(request, user)
        return redirect("home")
    return render(request, "app/signup.html", {"form": form})


@ratelimit(key='ip', rate='10/m', method='GET', block=True)
def signin(request: Any) -> HttpResponse:
    form = LogInForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            return redirect("home")
        form.add_error("password", "Incorrect credentials! Please check email or password!")
    return render(request, "app/login.html", {"form": form})


@ratelimit(key='ip', rate='10/m', method='GET', block=True)
def logout(request: Any) -> HttpResponse:
    django_logout(request)
    request.session.flush()
    return redirect("login")


@ratelimit(key='ip', rate='10/m', method='GET', block=True)
@login_required
def home(request: Any) -> HttpResponse:
    return render(request, "app/home.html")


@ratelimit(key='ip', rate='10/m', method='GET', block=True)
@login_required
def create_profile(request: Any) -> HttpResponse:
    user = MonUser.objects.get(id=request.user.id)
    form = ProfileForm(request.POST, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        profile = form.save(commit=False)
        profile.user = user
        profile.save()
        return redirect('profile')
    return render(request, "app/profile.html", {"form": form})


@ratelimit(key='ip', rate='10/m', method='GET', block=True)
@login_required
def edit_profile(request: Any) -> HttpResponse:
    user = MonUser.objects.get(id=request.user.id)
    profile = Profile.objects.get(user=user)
    if request.method == "POST":
        form = EditProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile.first_name = form.cleaned_data["first_name"]
            profile.last_name = form.cleaned_data["last_name"]
            profile.bio = form.cleaned_data["bio"]
            profile.birth_date = form.cleaned_data["birth_date"]
            if 'photo' in request.FILES:
                profile.photo = request.FILES['photo']
            profile.save()
            return redirect("profile")
    form = EditProfileForm(initial={
        "first_name": profile.first_name,
        "last_name": profile.last_name,
        "bio": profile.bio,
        "birth_date": profile.birth_date,
    })
    return render(request, "app/edit_profile.html", {"form": form})


@ratelimit(key='ip', rate='10/m', method='GET', block=True)
@login_required
def add_server(request: Any) -> HttpResponse:
    form = ServerCreateForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        server = form.save(commit=False)
        user = MonUser.objects.get(id=request.user.id)
        server.owner = user
        server.password = fernet.encrypt(form.cleaned_data["password"].encode()).decode()
        server.save()
        return redirect("server_details", server_id=server.id)
    return render(request, "app/add_server.html", {"form": form})


@login_required
def stop_monitoring(request, server_id):
    if server_id in active_monitoring_tasks:
        AsyncResult(active_monitoring_tasks[server_id]).revoke(terminate=True)
        del active_monitoring_tasks[server_id]
    return JsonResponse({"status": "Monitoring stopped"})


@ratelimit(key='ip', rate='10/m', method='GET', block=True)
@login_required
def server_details(request: Any, server_id: int) -> HttpResponse:
    server = Server.objects.get(id=server_id)
    if server.status != "❌Offline":
        server_stats.delay(server_id)
        r = redis.Redis(host='redis', port=6379, db=1, decode_responses=True)
        stats = r.hgetall(f"server:{server_id}")
        return render(request, "app/server_details.html", {"server": server,
                                                           "free_memory": [stats.get("free_memory"), "MB"],
                                                           "free_disk": [stats.get("free_disk"), "GB"],
                                                           "cpu_load": stats.get("cpu_load")})
    return render(request, "app/server_details.html", {"server": server,
                                                       "free_memory": ["❌Offline", ""],
                                                       "free_disk": ["❌Offline", ""],
                                                       "cpu_load": "❌Offline"})


@ratelimit(key='ip', rate='10/m', method='GET', block=True)
@login_required
def my_servers(request: Any) -> HttpResponse:
    user = MonUser.objects.get(id=request.user.id)
    servers = Server.objects.filter(owner=user).order_by('-created_at')
    return render(request, "app/my_servers.html", {"servers": servers})


@ratelimit(key='ip', rate='10/m', method='GET', block=True)
@login_required
def edit_server(request: Any, server_id: int) -> HttpResponse:
    server = Server.objects.get(id=server_id)
    form = ServerEditForm(request.POST or None, instance=server)
    if request.method == "POST" and form.is_valid():
        server.server_name = form.cleaned_data["server_name"]
        server.user_name = form.cleaned_data["password"]
        server.os_name = (form.cleaned_data["os_name"])
        server.server_ip = (form.cleaned_data["server_ip"])
        server.password = fernet.encrypt(form.cleaned_data["password"].encode()).decode()
        server.save()
        return redirect("server_details", server_id=server.id)
    return render(request, "app/edit_sever.html", {"form": form, "server": server})


@ratelimit(key='ip', rate='10/m', method='GET', block=True)
@login_required
def delete_server(request: Any, server_id: int) -> HttpResponseRedirect:
    if request.method == "GET":
        Server.objects.filter(id=server_id).delete()
        return redirect("my_servers")
