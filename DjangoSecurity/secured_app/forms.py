"""Module for Django Forms"""
from typing import Dict, Any
from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import CustomUser, Task


class SignupForm(forms.ModelForm):
    """
    A form for user registration.

    Handles user sign-up, ensuring unique usernames and emails, 
    along with password validation.
    """
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = CustomUser
        fields = ["username", "email", "password"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.TextInput(attrs={"class": "form-control"}),
            "password": forms.PasswordInput(attrs={"class": "form-control"})
        }

    def clean(self) -> Dict[str, Any]:
        """
        Validates the password and confirms it matches.

        Returns:
            Dict[str, Any]: The cleaned form data.

        Raises:
            ValidationError: If the password does not meet security requirements 
            or the confirmation password does not match.
        """
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_conf = cleaned_data.get("confirm_password")

        if password:
            try:
                validate_password(password)
            except ValidationError as e:
                self.add_error("password", e)

        if password_conf and password_conf != password:
            self.add_error("confirm_password", "Passwords do not match!")

        return cleaned_data

    def clean_email(self) -> str:
        """
        Ensures that the email is unique.

        Returns:
            str: The cleaned email.

        Raises:
            ValidationError: If the email is already in use.
        """
        email = self.cleaned_data["email"]
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use. Please sign in or use a different email.")
        return email

    def clean_username(self) -> str:
        """
        Ensures that the username is unique.

        Returns:
            str: The cleaned username.

        Raises:
            ValidationError: If the username is already taken.
        """
        username = self.cleaned_data["username"]
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already in use. Please choose another one.")
        return username


class SigninForm(forms.Form):
    """
    A form for user login.

    Ensures the provided username exists before authentication.
    """
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))

    def clean_username(self) -> str:
        """
        Validates the username.

        Returns:
            str: The cleaned username.

        Raises:
            ValidationError: If the username does not exist in the system.
        """
        username = self.cleaned_data["username"]
        if not CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("This username does not exist. Please check and try again.")
        return username


class TaskForm(forms.ModelForm):
    """
    A form for creating and updating tasks.

    Ensures title length, non-empty description, and valid due dates.
    """

    class Meta:
        model = Task
        fields = "__all__"
        exclude = ["user"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "due_date": forms.DateInput(attrs={"type": "date", "class": "form-control"})
        }

    def clean_title(self) -> str:
        """
        Ensures the task title does not exceed 50 characters.

        Returns:
            str: The cleaned title.

        Raises:
            ValidationError: If the title exceeds 50 characters.
        """
        title = self.cleaned_data["title"]
        if len(title) > 50:
            raise forms.ValidationError("The title may not be longer than 50 characters.")
        return title

    def clean_description(self) -> str:
        """
        Ensures the task description is not empty.

        Returns:
            str: The cleaned description.

        Raises:
            ValidationError: If the description is empty.
        """
        description = self.cleaned_data["description"]
        if not description:
            raise forms.ValidationError("The description may not be empty.")
        return description

    def clean_due_date(self) -> Any:
        """
        Ensures the due date is not in the past.

        Returns:
            Any: The cleaned due date.

        Raises:
            ValidationError: If the due date is before today.
        """
        due_date = self.cleaned_data["due_date"]
        if due_date < timezone.localdate():
            raise forms.ValidationError("The due date cannot be in the past.")
        return due_date
