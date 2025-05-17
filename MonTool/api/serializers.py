import os

from cryptography.fernet import Fernet
from django.contrib.auth import authenticate
from rest_framework import serializers


from app.models import MonUser, Server

fernet = Fernet(os.getenv("ENCRYPTION_KEY").encode())

class SignupSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)

    class Meta:
        model = MonUser
        fields=("email", "password")

    def create(self, validated_data):
        user = MonUser.objects.create(email=validated_data["email"])
        user.set_password(validated_data["password"])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email=serializers.EmailField()
    password=serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(email=attrs["email"], password=attrs["password"])
        if not user:
            raise serializers.ValidationError("Invalid credentials!")
        attrs["user"] = user
        return attrs

    def create(self, validated_data):
        return  validated_data["user"]


class AddServerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Server
        fields=("server_name", "user_name", "server_ip", "password", "os_name")

    def create(self, validated_data):
        validated_data["password"]=fernet.encrypt(validated_data["password"].encode()).decode()
        return Server.objects.create(**validated_data)

class ListServersSerializer(serializers.ModelSerializer):
    class Meta:
        model=Server
        fields="__all__"

