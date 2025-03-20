"""Forms Module"""
from django import forms
from django.contrib.auth.password_validation import validate_password, password_validators_help_texts
from board.models import User
from django.forms import ValidationError
from .models import UserProfile


class RegistrationForm(forms.ModelForm):
    """
    A form for user registration, including username, email, password,
    and password confirmation. Validates that the password meets the
    required criteria and that the email and username are unique.

    Attributes:
        confirm_password: A field to confirm the user's password.
    """
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.TextInput(attrs={"class": "form-control"}),
            "password": forms.PasswordInput(attrs={"class": "form-control"})
        }

    def clean(self) -> dict:
        """
        Validates the password and confirms that the password and
        confirmation password match.

        Returns:
            dict: The cleaned data.
        """
        password = self.cleaned_data["password"]
        password_conf = self.cleaned_data["confirm_password"]
        try:
            validate_password(password)
        except ValidationError:
            self.add_error("password", password_validators_help_texts(password_validators=None))
        if password_conf != password:
            self.add_error("confirm_password", "Password mismatch! Please check the password in both fields.")
        return self.cleaned_data

    def clean_email(self) -> str:
        """
        Validates that the email address is unique in the database.

        Returns:
            str: The cleaned email address.

        Raises:
            ValidationError: If the email is already in use.
        """
        email = self.cleaned_data["email"]
        user_emails = User.objects.values_list("email", flat=True)
        if email in user_emails:
            raise ValidationError("The email inserted is already used! "
                                  "Please sign in or use a different email for sign up.")
        return email

    def clean_username(self) -> str:
        """
        Validates that the username is unique in the database.

        Returns:
            str: The cleaned username.

        Raises:
            ValidationError: If the username is already in use.
        """
        username = self.cleaned_data["username"]
        usernames = User.objects.values_list("username", flat=True)
        if username in usernames:
            raise ValidationError("The username inserted is already used! "
                                  "Please sign in or use another one.")
        return username


class UserProfileForm(forms.ModelForm):
    """
    A form for updating user profile information, excluding the user
    field and including the birth date with a date input widget.

    Attributes:
        birth_date: The user's birth date.
    """
    class Meta:
        model = UserProfile
        fields = '__all__'
        exclude = ["user"]
        widgets = {
            "birth_date": forms.DateInput(attrs={"type": "date"})
        }


class ChangePasswordForm(forms.Form):
    """
    A form for changing the user's password, including fields for
    the current password and the new password.

    Attributes:
        current_password: The user's current password.
        new_password: The user's new password.
    """
    current_password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))

