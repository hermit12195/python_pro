from django.utils import timezone
from rest_framework import serializers
from .models import Task, CustomUser


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model=Task
        exclude=["user"]

    def validate(self, data):
        if len(data["title"]) > 50:
            raise serializers.ValidationError("Title should not exceed 50 characters.")
        if data["description"] is None:
            raise serializers.ValidationError("The description may not be empty.")
        if data["due_date"] < timezone.localdate():
            raise serializers.ValidationError("The Due Date may not be less than the current date.")
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields="__all__"

