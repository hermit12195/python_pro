"""Views module"""
import logging
from datetime import datetime
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.http import Http404
from .forms import RegistrationForm, UserProfileForm, ChangePasswordForm
from board.models import User
from .models import UserProfile


def register_view(request) -> HttpResponse:
    """
    Handles user registration. If the form is valid, saves the new user
    and redirects to their profile page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: A redirect to the profile view or a render of the signup page.
    """
    try:
        if request.method == "POST":
            form = RegistrationForm(request.POST)
            if form.is_valid():
                logging.info(f"{datetime.utcnow().replace(microsecond=0)} - {form.cleaned_data}")
                form.save()
                username = form.cleaned_data["username"]
                return redirect("profile_view", username)

            logging.error(f"{datetime.utcnow().replace(microsecond=0)} - {form.errors}")
        return render(request, "userprofile/signup.html", {"form":
                                                               (RegistrationForm(request.POST) if request.POST
                                                                else RegistrationForm())})
    except Http404 as e:
        logging.error(f"{datetime.utcnow().replace(microsecond=0)} - {e.__str__()}")


def profile_view(request, username: str) -> HttpResponse:
    """
    Displays the profile page for a specific user.

    Args:
        request (HttpRequest): The HTTP request object.
        username (str): The username of the user whose profile is being viewed.

    Returns:
        HttpResponse: The rendered profile page with user data.
    """
    try:
        user_id = User.objects.filter(username=username).values_list('id', flat=True).first()
        user = UserProfile.objects.filter(user_id=user_id).values()[0]
        bio, birth_date, location = user["bio"], user["birth_date"], user["location"]
        user_profile = UserProfile.objects.select_related("user").filter(user__username=username).first()
        avatar_url = user_profile.avatar.url
        if birth_date is None:
            birth_date = "No birthday yet!"
        return render(request, "userprofile/profile.html", {"username": username, "bio": bio,
                                                            "birth_date": birth_date, "location": location,
                                                            "avatar": avatar_url})
    except Http404 as e:
        logging.error(f"{datetime.utcnow().replace(microsecond=0)} - {e.__str__()}")


def edit_profile(request, username: str) -> HttpResponse:
    """
    Allows a user to edit their profile details, such as bio, birth date, and location.

    Args:
        request (HttpRequest): The HTTP request object.
        username (str): The username of the user whose profile is being edited.

    Returns:
        HttpResponse: A redirect to the profile view or the edit profile page.
    """
    try:
        user = User.objects.get(username=username)
        user_profile = UserProfile.objects.get(user=user)
        if request.method == "POST":
            form = UserProfileForm(request.POST, instance=user_profile)
            if form.is_valid():
                form.save()
                logging.info(f"{datetime.utcnow().replace(microsecond=0)} - {form.cleaned_data}")
                return redirect("profile_view", username)
            print(form.errors)

        form = UserProfileForm(instance=user_profile)
        return render(request, "userprofile/edit_profile.html", {"form": form, "username": username})
    except Http404 as e:
        logging.error(f"{datetime.utcnow().replace(microsecond=0)} - {e.__str__()}")


def change_pass(request, username: str) -> HttpResponse:
    """
    Allows a user to change their password. Validates the current password and ensures
    the new password is not the same as the current one.

    Args:
        request (HttpRequest): The HTTP request object.
        username (str): The username of the user changing their password.

    Returns:
        HttpResponse: A redirect to the profile view or a render of the change password page.
    """
    try:
        if request.method == "POST":
            form = ChangePasswordForm(request.POST)
            user_password = User.objects.filter(username=username).values_list("password", flat=True).first()
            if form.is_valid():
                if user_password != form.cleaned_data["current_password"]:
                    messages.error(request, "Incorrect current password!")
                    logging.info(f"{datetime.utcnow().replace(microsecond=0)} - Incorrect current password!")
                elif user_password == form.cleaned_data["new_password"]:
                    messages.error(request, "The new password inserted is already used! Please use a different one.")
                    logging.info(f"{datetime.utcnow().replace(microsecond=0)} - The new password inserted is already used!")
                else:
                    User.objects.filter(username=username).update(password=form.cleaned_data["new_password"])
                    logging.info(f"{datetime.utcnow().replace(microsecond=0)} - The Password was successfully changed!")
                    messages.info(request, "The password was successfully changed!")
                    return redirect("profile_view", username)
        form = ChangePasswordForm()
        return render(request, "userprofile/change_pass.html", {"form": form, "username": username})
    except Http404 as e:
        logging.error(f"{datetime.utcnow().replace(microsecond=0)} - {e.__str__()}")
