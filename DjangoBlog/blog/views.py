from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout as django_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django_ratelimit.decorators import ratelimit
from typing import Any

from blog.forms import SignUpForm, LogInForm, PostCreateForm, PostEditForm, ProfileForm, EditProfileForm
from blog.models import BlogUser, Post, Comment, Profile
from celery_tasks.tasks import signup_email, adv_email


@ratelimit(key='ip', rate='10/m', method='GET', block=True)
def signup(request: Any) -> HttpResponse:
    """
    Handles user signup. If the form is valid, the user is created and logged in.

    Args:
        request (Any): The HTTP request object.

    Returns:
        HttpResponse: Redirects to the feed page after successful signup.
    """
    form = SignUpForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data["password"])
        user.save()
        login(request, user)
        signup_email.delay(user.id)
        adv_email.apply_async(kwargs={"user_id": user.id}, countdown=600)
        return redirect("feed", user.username)
    return render(request, "blog/signup.html", {"form": form})


@ratelimit(key='ip', rate='10/m', method='GET', block=True)
def signin(request: Any) -> HttpResponse:
    """
    Handles user login. If the credentials are correct, the user is logged in and redirected to the feed.

    Args:
        request (Any): The HTTP request object.

    Returns:
        HttpResponse: Redirects to the feed page after successful login.
    """
    form = LogInForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("feed", user)
        form.add_error("password", "Incorrect credentials! Please check email or password!")
    return render(request, "blog/login.html", {"form": form})


@ratelimit(key='ip', rate='10/m', method='GET', block=True)
@login_required
def feed(request: Any, username: str) -> HttpResponse:
    """
    Displays the feed with posts created today, ordered by the latest.

    Args:
        request (Any): The HTTP request object.
        username (str): The username of the logged-in user.

    Returns:
        HttpResponse: Renders the feed template with posts.
    """
    posts = Post.objects.filter(created_datetime__day=timezone.now().day).order_by("-created_datetime")
    return render(request, "blog/feed.html", {"username": username, "posts": posts})


@ratelimit(key='ip', rate='10/m', method='GET', block=True)
@login_required
def create_profile(request: Any, username: str) -> HttpResponse:
    """
    Creates or updates the profile for a given user.

    Args:
        request (Any): The HTTP request object.
        username (str): The username of the user whose profile is being created or edited.

    Returns:
        HttpResponse: Redirects to the user's profile page after saving the profile.
    """
    user = BlogUser.objects.get(username=username)
    form = ProfileForm(request.POST, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        profile = form.save(commit=False)
        profile.user = user
        profile.save()
        return redirect('profile', username=username)
    return render(request, "blog/profile.html", {"user": user, "form": form})


@ratelimit(key='ip', rate='10/m', method='GET', block=True)
@login_required
def edit_profile(request: Any, username: str) -> HttpResponse:
    """
    Edits the profile of a given user.

    Args:
        request (Any): The HTTP request object.
        username (str): The username of the user whose profile is being edited.

    Returns:
        HttpResponse: Redirects to the user's profile page after updating the profile.
    """
    user = BlogUser.objects.get(username=username)
    profile = Profile.objects.get(user=user)
    form = EditProfileForm(request.POST, request.FILES or None, instance=profile)
    if request.method == "POST" and form.is_valid():
        profile.first_name = form.cleaned_data["first_name"]
        profile.last_name = form.cleaned_data["last_name"]
        profile.bio = form.cleaned_data["bio"]
        profile.birth_date = form.cleaned_data["birth_date"]
        if 'photo' in request.FILES:
            profile.photo = request.FILES['photo']
        profile.save()
        return redirect("profile", username=username)
    return render(request, "blog/edit_profile.html", {"username": username, "form": form})


@ratelimit(key='ip', rate='10/m', method='GET', block=True)
@login_required
def create_post(request: Any, username: str) -> HttpResponse:
    """
    Allows the user to create a new post.

    Args:
        request (Any): The HTTP request object.
        username (str): The username of the logged-in user.

    Returns:
        HttpResponse: Redirects to the post details page after creating the post.
    """
    form = PostCreateForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        post = form.save(commit=False)
        user = BlogUser.objects.get(username=username)
        post.user = user
        post.save()
        tags = form.cleaned_data["tag"]
        post.tag.set(tags)
        return redirect("post_details", username=user.username, id=post.id)
    return render(request, "blog/create_post.html", {"username": username, "form": form})


@ratelimit(key='ip', rate='10/m', method='GET', block=True)
@login_required
def post_detail(request: Any, username: str, id: int) -> HttpResponse:
    """
    Displays the details of a specific post.

    Args:
        request (Any): The HTTP request object.
        username (str): The username of the logged-in user.
        id (int): The ID of the post to display.

    Returns:
        HttpResponse: Renders the post detail template.
    """
    post = Post.objects.get(id=id)
    return render(request, "blog/post_details.html", {"post": post, "username": username})


@ratelimit(key='ip', rate='10/m', method='GET', block=True)
@login_required
def my_posts(request: Any, username: str) -> HttpResponse:
    """
    Displays all posts created by the logged-in user.

    Args:
        request (Any): The HTTP request object.
        username (str): The username of the logged-in user.

    Returns:
        HttpResponse: Renders the template displaying the user's posts.
    """
    user = BlogUser.objects.get(username=username)
    posts = Post.objects.filter(user=user).order_by('-created_datetime')
    return render(request, "blog/my_posts.html", {"posts": posts, "username": username})


@ratelimit(key='ip', rate='10/m', method='GET', block=True)
@login_required
def edit_post(request: Any, username: str, id: int) -> HttpResponse:
    """
    Edits the details of a specific post.

    Args:
        request (Any): The HTTP request object.
        username (str): The username of the logged-in user.
        id (int): The ID of the post to edit.

    Returns:
        HttpResponse: Redirects to the post detail page after updating the post.
    """
    post = Post.objects.get(id=id)
    form = PostEditForm(request.POST or None, initial={
        "title": post.title,
        "plot": post.plot,
        "tag": str([tag.name for tag in post.tag.all()]).strip("[]").replace("'", "")
    })
    if request.method == "POST" and form.is_valid():
        post.title = form.cleaned_data["title"]
        post.plot = form.cleaned_data["plot"]
        post.category.set(form.cleaned_data["category"])
        post.tag.set(form.cleaned_data["tag"])
        post.save()
        return redirect("post_details", username=username, id=post.id)
    return render(request, "blog/edit_post.html", {"username": username, "form": form, "post": post})


@ratelimit(key='ip', rate='10/m', method='GET', block=True)
@login_required
def delete_post(request: Any, username: str, id: int) -> HttpResponse:
    """
    Deletes a specific post.

    Args:
        request (Any): The HTTP request object.
        username (str): The username of the logged-in user.
        id (int): The ID of the post to delete.

    Returns:
        HttpResponse: Redirects to the user's posts page after deletion.
    """
    if request.method == "GET":
        Post.objects.filter(id=id).delete()
        return redirect("my_posts", username=username)


@ratelimit(key='ip', rate='10/m', method='GET', block=True)
def logout(request: Any) -> HttpResponse:
    """
    Logs out the user and redirects them to the login page.

    Args:
        request (Any): The HTTP request object.

    Returns:
        HttpResponse: Redirects to the login page after logging out.
    """
    django_logout(request)
    request.session.flush()
    return redirect("login")


@ratelimit(key='ip', rate='10/m', method='GET', block=True)
@login_required
def comment(request: Any, username: str, id: int) -> HttpResponse:
    """
    Allows the user to comment on a specific post.

    Args:
        request (Any): The HTTP request object.
        username (str): The username of the logged-in user.
        id (int): The ID of the post to comment on.

    Returns:
        HttpResponse: Redirects to the feed page after submitting the comment.
    """
    user = BlogUser.objects.get(username=username)
    post = get_object_or_404(Post, id=id)
    if request.method == "POST":
        plot = request.POST.get("comment")
        if plot:
            Comment.objects.create(plot=plot, user=user, post=post)
        return redirect('feed', username=username)
