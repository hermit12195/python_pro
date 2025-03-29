from django.utils import timezone
from rest_framework import serializers
from .models import Task, CustomUser


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the CustomUser model.

    This serializer handles the serialization and deserialization of the CustomUser model.
    It includes all fields from the model.

    Meta:
        model (CustomUser): The model to serialize.
        fields (str): All fields of the CustomUser model are included in the serialized output.
    """

    class Meta:
        model = CustomUser
        fields = "__all__"


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for the Task model.

    This serializer handles the serialization and deserialization of the Task model.
    It includes fields for the task title, description, due date, and associated user.

    Attributes:
        user (UserSerializer): Nested UserSerializer to include user information in the task representation.

    Meta:
        model (Task): The model to serialize.
        fields (list): The list of fields to include in the serialized output.
    """

    user: UserSerializer = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ["title", "description", "due_date", "user"]

    def validate(self, data: dict) -> dict:
        """
        Custom validation for the TaskSerializer.

        This method validates the task data before saving it. It checks that:
        - The title is not longer than 50 characters.
        - The description is not empty.
        - The due date is not in the past.

        Args:
            data (dict): The data to validate.

        Returns:
            dict: The validated data.

        Raises:
            ValidationError: If any validation fails.
        """

        if len(data["title"]) > 50:
            raise serializers.ValidationError("Title should not exceed 50 characters.")

        if data["description"] is None:
            raise serializers.ValidationError("The description may not be empty.")

        if data["due_date"] < timezone.localdate():
            raise serializers.ValidationError("The Due Date may not be less than the current date.")

        return data




