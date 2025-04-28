from typing import Dict
from django import forms

from django.contrib.auth.password_validation import validate_password

from .models import BlogUser, Post, Category, Profile


class SignUpForm(forms.ModelForm):
    """
    Form for signing up a new BlogUser.

    Attributes:
        confirm_password (forms.CharField): Confirmation password field.
    """
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))

    class Meta:
        model = BlogUser
        fields = ["username", "email", "password"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.TextInput(attrs={"class": "form-control"}),
            "password": forms.PasswordInput(attrs={"class": "form-control"})
        }

    def clean(self) -> Dict[str, str]:
        """
        Validates the password and ensures both password fields match.

        Returns:
            Dict[str, str]: Cleaned data if validation passes.
        """
        password = self.cleaned_data["password"]
        confirm_password = self.cleaned_data["confirm_password"]
        try:
            validate_password(password)
        except Exception as e:
            self.add_error("password", e)
        if password != confirm_password:
            self.add_error("confirm_password", "Password mismatch! Please check the password in both fields.")
        return self.cleaned_data

    def clean_email(self) -> str:
        """
        Validates that the email is not already in use by another BlogUser.

        Returns:
            str: Cleaned email.
        """
        email = self.cleaned_data["email"]
        if BlogUser.objects.filter(email__contains=email).exists():
            self.add_error("email", "The email inserted is already used! "
                                    "Please sign in or use a different email for sign up.")
        return email

    def clean_username(self) -> str:
        """
        Validates that the username is not already taken by another BlogUser.

        Returns:
            str: Cleaned username.
        """
        username = self.cleaned_data["username"]
        if BlogUser.objects.filter(username__contains=username).exists():
            self.add_error("username", "The username inserted is already used! "
                                       "Please sign in or use another one.")
        return username


class LogInForm(forms.Form):
    """
    Form for logging in a BlogUser.

    Attributes:
        username (forms.CharField): Username field.
        password (forms.CharField): Password field.
    """
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))

    def clean_username(self) -> str:
        """
        Validates that the username exists in the system.

        Returns:
            str: Cleaned username.
        """
        username = self.cleaned_data["username"]
        if not BlogUser.objects.filter(username__contains=username).exists():
            self.add_error("username", "Username does not exist. Please check and try again.")
        return username


class PostCreateForm(forms.ModelForm):
    """
    Form for creating a new Post.
    """

    class Meta:
        model = Post
        fields = ["title", "plot", "tag", "category"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "plot": forms.Textarea(attrs={"class": "form-control"}),
            "tag": forms.TextInput(attrs={"class": "form-control"})
        }

    def __init__(self, *args, **kwargs):
        """
        Initializes the form and sets up the category choices.
        """
        super().__init__(*args, **kwargs)
        categories = Category.objects.all() if len(Category.objects.all()) > 0 else []
        self.fields["category"] = forms.ChoiceField(choices=[(category.id, category.title) for category in categories],
                                                    widget=forms.Select(attrs={"class": "form-control"}))


class PostEditForm(forms.ModelForm):
    """
    Form for editing an existing Post.
    """

    class Meta:
        model = Post
        fields = ["title", "plot", "tag", "category"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "plot": forms.Textarea(attrs={"class": "form-control"}),
            "tag": forms.TextInput(attrs={"class": "form-control"})
        }

    def __init__(self, *args, **kwargs):
        """
        Initializes the form and sets up the category choices for editing.
        """
        super().__init__(*args, **kwargs)
        categories = Category.objects.all() if len(Category.objects.all()) > 0 else []
        self.fields["category"] = forms.ChoiceField(choices=[(category.id, category.title) for category in categories],
                                                    widget=forms.Select(attrs={"class": "form-control"}))


class ProfileForm(forms.ModelForm):
    """
    Form for creating or updating a Profile for a BlogUser.
    """

    class Meta:
        model = Profile
        fields = "__all__"
        exclude = ["user"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "bio": forms.TextInput(attrs={"class": "form-control"}),
            "birth_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "photo": forms.FileInput(attrs={"class": "form-control"})
        }


class EditProfileForm(forms.ModelForm):
    """
    Form for editing an existing Profile of a BlogUser.
    """

    class Meta:
        model = Profile
        fields = "__all__"
        exclude = ["user"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "bio": forms.TextInput(attrs={"class": "form-control"}),
            "birth_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "photo": forms.FileInput(attrs={"class": "form-control"})
        }
