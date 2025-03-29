import sqlite3
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_protect
from django_ratelimit.decorators import ratelimit
from django.http import HttpRequest, HttpResponse
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .forms import SignupForm, SigninForm, TaskForm
from .models import Task, CustomUser
from .serializers import TaskSerializer, UserSerializer


@ratelimit(key='ip', rate='10/m', method='POST', block=True)
@csrf_protect
def signup_view(request: HttpRequest) -> HttpResponse:
    """
    Handle user signup.

    Validates the signup form, creates a new user, sets the password, and logs in the user.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: A redirect to the 'home' view on successful signup, or the rendered signup form on failure.
    """
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            login(request, user)
            username = form.cleaned_data["username"]
            return redirect("home", username)
    return render(request, "secured_app/signup.html", {"form": SignupForm(request.POST) if request.POST else SignupForm()})


@ratelimit(key='ip', rate='10/m', method='POST', block=True)
@csrf_protect
def signin_view(request: HttpRequest) -> HttpResponse:
    """
    Handle user signin.

    Validates the signin form, authenticates the user, and logs them in if credentials are correct.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: A redirect to the 'home' view on successful signin, or the rendered signin form with error messages on failure.
    """
    form = SigninForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("home", user)
        form.add_error("password", "Incorrect credentials! Please check email or password!")
    return render(request, "secured_app/signin.html", {"form": form})


@ratelimit(key='ip', rate='10/m', method='GET', block=True)
def logout_view(request: HttpRequest) -> HttpResponse:
    """
    Handle user logout.

    Logs out the user, clears the session, and redirects to the signin page.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: A redirect to the 'signin' page.
    """
    logout(request)
    request.session.flush()
    return redirect("signin")


@ratelimit(key='ip', rate='10/m', method='GET', block=True)
@csrf_protect
def home_view(request: HttpRequest, username: str) -> HttpResponse:
    """
    Display the home page for an authenticated user.

    Fetches and displays the email associated with the logged-in user's username.

    Args:
        request: The HTTP request object.
        username: The username of the logged-in user.

    Returns:
        HttpResponse: The rendered home page template with user data.
    """
    form=TaskForm(request.POST or None)
    user=CustomUser.objects.get(username=request.user)
    if request.method == "POST":
        if form.is_valid():
            task = form.save(commit=False)
            task.user = user
            title = form.cleaned_data["title"]
            task.save()
            return redirect("task_detail", user, title)
    conn = sqlite3.connect('db.sqlite3')
    curs = conn.cursor()
    curs.execute("SELECT email FROM secured_app_customuser WHERE username=?", (user.username,))
    email = curs.fetchone()
    return render(request, "secured_app/home.html", {"user": user, "email": email, "form": form})


def task_detail_view(request, username, title):
    record = Task.objects.get(user__username=username, title=title)
    return render(request, "secured_app/task_details.html", {"record": record})


class TaskView(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserView(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]




