from typing import Dict
from django import forms

from django.contrib.auth.password_validation import validate_password

from app.models import MonUser, Server, Profile


class SignUpForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))

    class Meta:
        model = MonUser
        fields = ["email", "password"]
        widgets = {
            "email": forms.TextInput(attrs={"class": "form-control"}),
            "password": forms.PasswordInput(attrs={"class": "form-control"})
        }

    def clean(self) -> Dict[str, str]:
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
        email = self.cleaned_data["email"]
        if MonUser.objects.filter(email__contains=email).exists():
            self.add_error("email", "The email inserted is already used! "
                                    "Please sign in or use a different email for sign up.")
        return email


class LogInForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))

    def clean_email(self) -> str:
        email = self.cleaned_data["email"]
        if not MonUser.objects.filter(email__contains=email).exists():
            self.add_error("email", "Email is not registered. Please check and try again.")
        return email


class ServerCreateForm(forms.ModelForm):
    class Meta:
        model = Server
        fields = ["server_name", "user_name","server_ip", "password"]
        widgets = {
            "server_name": forms.TextInput(attrs={"class": "form-control"}),
            "user_name": forms.TextInput(attrs={"class": "form-control"}),
            "server_ip": forms.TextInput(attrs={"class": "form-control"}),
            "password": forms.PasswordInput(attrs={"class": "form-control"})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["os_name"] = forms.ChoiceField(choices=[("Windows", "Windows"), ("Linux", "Linux")],
                                                    widget=forms.Select(attrs={"class": "form-control"}))


class ServerEditForm(forms.ModelForm):
    class Meta:
        model = Server
        fields = ["server_name", "user_name", "server_ip", "password"]
        widgets = {
            "server_name": forms.TextInput(attrs={"class": "form-control"}),
            "user_name": forms.TextInput(attrs={"class": "form-control"}),
            "server_ip": forms.TextInput(attrs={"class": "form-control"}),
            "password": forms.PasswordInput(attrs={"class": "form-control"})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["os_name"] = forms.ChoiceField(choices=[("Windows", "Windows"), ("Linux", "Linux")],
                                                   widget=forms.Select(attrs={"class": "form-control"}))


class ProfileForm(forms.ModelForm):
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
