import sqlite3
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_protect
from django_ratelimit.decorators import ratelimit
from .forms import SignupForm, SigninForm
from django.http import HttpRequest, HttpResponse



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
    user = request.user
    conn = sqlite3.connect('db.sqlite3')
    curs = conn.cursor()
    curs.execute("SELECT email FROM secured_app_customuser WHERE username=?", (user.username,))
    email = curs.fetchone()
    return render(request, "secured_app/home.html", {"user": user, "email": email})
