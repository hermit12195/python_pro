import base64
import json
from typing import Any
from django.test import TestCase
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIClient
from rest_framework.response import Response
from .models import CustomUser, Task
from .forms import SignupForm, TaskForm


class TaskFormTest(TestCase):
    """Tests for validating the TaskForm."""

    def setUp(self) -> None:
        """Creates a test user and a test task before each test."""
        self.user = CustomUser.objects.create(
            username="tes123t111211233name",
            email="123t21131123est@123test.com",
            password="testpassword"
        )
        self.form = TaskForm(data={
            "title": "test",
            "description": "test1123@test.com",
            "due_date": "2025-03-30"
        })
        task = self.form.save(commit=False)
        task.user = self.user
        task.save()

    def test_form(self) -> None:
        """Checks if the task description is stored correctly."""
        self.assertEqual(
            Task.objects.filter(title="test").values_list("description", flat=True)[0],
            "test1123@test.com"
        )

    def test_long_title(self) -> None:
        """Ensures that the form does not accept overly long titles."""
        form = TaskForm(data={
            "title": "t" * 100,  # Exceeding allowed length
            "description": "test1123@test.com",
            "due_date": "2025-03-30"
        })
        self.assertFalse(form.is_valid())

    def test_none_title(self) -> None:
        """Ensures the form does not accept a `None` title."""
        form = TaskForm(data={
            "title": None,
            "description": "test1123@test.com",
            "due_date": "2025-03-30"
        })
        self.assertFalse(form.is_valid())

    def test_false_date(self) -> None:
        """Ensures that past dates are not accepted."""
        form = TaskForm(data={
            "title": "test",
            "description": "test1123@test.com",
            "due_date": "2025-03-28"
        })
        self.assertFalse(form.is_valid())


class TestTaskAPI(TestCase):
    """API tests for the Task model."""

    def setUp(self) -> None:
        """Creates a test user and authenticates them."""
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            username="tes123t111211233name",
            email="123t21131123est@123test.com",
            password="testpassword"
        )
        self.client.force_authenticate(user=self.user)

    def test_positive_create(self) -> None:
        """Checks if a task is successfully created."""
        data = {
            "title": "1test1",
            "description": "test1123@test.com",
            "due_date": "2025-03-30"
        }
        response: Response = self.client.post("/api/tasks/", data, format="json")
        self.assertEqual(response.status_code, 201)

    def test_negative_create(self) -> None:
        """Ensures that a task with an overly long title cannot be created."""
        data = {
            "title": "t" * 100,
            "description": "test1123@test.com",
            "due_date": "2025-03-30"
        }
        response: Response = self.client.post("/api/tasks/", data, format="json")
        self.assertEqual(response.status_code, 400)  # Expect validation error

    def test_description_none(self) -> None:
        """Ensures that a task cannot have an empty description."""
        data = {
            "title": "ValidTitle",
            "description": None,
            "due_date": "2025-03-30"
        }
        response: Response = self.client.post("/api/tasks/", data, format="json")
        self.assertEqual(response.status_code, 400)  # Expect error

    def test_false_due_date(self) -> None:
        """Ensures that a task cannot be created with a past due date."""
        data = {
            "title": "ValidTitle",
            "description": "Some description",
            "due_date": "2025-03-28"
        }
        response: Response = self.client.post("/api/tasks/", data, format="json")
        self.assertEqual(response.status_code, 400)  # Expect error


class TestUserAPI(TestCase):
    """API tests for the User model."""

    def setUp(self) -> None:
        """Creates a test user."""
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            username="tes123t111211233name",
            email="123t21131123est@123test.com",
            password="testpassword"
        )

    def test_users_list(self) -> None:
        """Checks if the user list is accessible for authenticated users."""
        credentials = "tes123t111211233name:testpassword"
        encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")

        response: Response = self.client.get(
            "/api/users/",
            HTTP_AUTHORIZATION=f"Basic {encoded_credentials}"
        )
        self.assertEqual(response.status_code, 200)
