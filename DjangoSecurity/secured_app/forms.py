from http.cookiejar import UTC_ZONES

from django import forms
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser, Task
from django.utils import timezone

class SignupForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))

    class Meta:
        model = CustomUser
        fields = ["username", "email", "password"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.TextInput(attrs={"class": "form-control"}),
            "password": forms.PasswordInput(attrs={"class": "form-control"})
        }

    def clean(self) -> dict:
        """
        Validates the password and confirms the password match.

        Ensures that the password meets the requirements and that the
        confirm_password field matches the password.

        Returns:
            dict: The cleaned data for the form.
        """
        password = self.cleaned_data["password"]
        password_conf = self.cleaned_data["confirm_password"]
        try:
            validate_password(password)
        except Exception as e:
            self.add_error("password", e)
        if password_conf != password:
            self.add_error("confirm_password", "Password mismatch! Please check the password in both fields.")
        return self.cleaned_data

    def clean_email(self) -> str:
        """
        Validates that the email is unique.

        Checks if the email is already used by another user.

        Returns:
            str: The cleaned email address.

        Raises:
            ValidationError: If the email is already in use.
        """
        email = self.cleaned_data["email"]
        if email in CustomUser.objects.values_list("email", flat=True):
            self.add_error("email", "The email inserted is already used! "
                                    "Please sign in or use a different email for sign up.")
        return email

    def clean_username(self) -> str:
        """
        Validates that the username is unique in the database.

        Checks if the username is already taken by another user.

        Returns:
            str: The cleaned username.

        Raises:
            ValidationError: If the username is already in use.
        """
        username = self.cleaned_data["username"]
        usernames = CustomUser.objects.values_list("username", flat=True)
        if username in usernames:
            self.add_error("username", "The username inserted is already used! "
                                      "Please sign in or use another one.")
        return username


class SigninForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))

    def clean_username(self) -> str:
        """
        Validates the username provided in the sign-in form.

        Checks if the username exists in the system, and raises an error
        if not found.

        Returns:
            str: The cleaned username.

        Raises:
            ValidationError: If the username does not exist in the system.
        """
        username = self.cleaned_data["username"]
        if not CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("Username does not exist. Please check and try again.")
        return username


class TaskForm(forms.ModelForm):
    class Meta:
        model=Task
        fields="__all__"
        exclude = ["user"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "due_date": forms.DateInput(attrs={"type": "date", "class": "form-control"})
        }

    def clean_title(self):
        title=self.cleaned_data["title"]
        if len(title)>50:
            self.add_error("title", "The title may not be longer than 50 characters.")
        return  title

    def clean_description(self):
        description=self.cleaned_data["description"]
        if description is None:
            self.add_error("description", "The description may not be empty.")
        return description

    def clean_due_date(self):
        due_date=self.cleaned_data["due_date"]
        if due_date < timezone.localdate():
            self.add_error("due_date", "The Due Date may not be less than the current date.")
        return due_date


