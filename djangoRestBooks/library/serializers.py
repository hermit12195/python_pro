"""Serializers Module"""
from rest_framework import serializers
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.

    This serializer converts the Book model instances to JSON format and vice versa.
    It automatically handles validation and serialization of fields in the Book model.

    Attributes:
        class Meta:
            model (Book): The model to serialize (Book).
            fields (list): A list of fields from the model to include in the serialization, in this case, all fields.
    """

    class Meta:
        model = Book
        fields = "__all__"
