import base64
import json
from django.test import TestCase
from rest_framework.exceptions import ValidationError
from .models import CustomUser, Task
from .forms import SignupForm, TaskForm
from rest_framework.test import APIClient



"""class ModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username="tes123t111211233name", email="123t21131123est@123test.com",
                                              password="testpassword")

    def test_user_creation(self):
        self.assertEqual(self.user.username, "tes123t111211233name")


class FormTest(TestCase):
    def setUp(self):
        self.form = SignupForm(data={
            "username": "test",
            "email": "test1123@test.com",
            "password": "P123456789$",
            "confirm_password": "P123456789$"})

    def test_signup(self):
        self.assertTrue(self.form.is_valid())


class ViewTest(TestCase):
    def test_signin(self):
        response = self.client.get(reverse("signin"))
        self.assertEqual(response.status_code, 200)
   """


class TaskFormTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username="tes123t111211233name", email="123t21131123est@123test.com",
                                              password="testpassword")
        self.form = TaskForm(data={
            "title": "test",
            "description": "test1123@test.com",
            "due_date": "2025-03-30"})
        task=self.form.save(commit=False)
        task.user=self.user
        task.save()

    def test_form(self):
        self.assertEqual(Task.objects.filter(title="test").values_list("description", flat=True)[0], "test1123@test.com")

    def test_long_title(self):
        form = TaskForm(data={
            "title": "testtesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttest",
            "description": "test1123@test.com",
            "due_date": "2025-03-30"})
        self.assertFalse(form.is_valid())

    def test_None_description(self):
        form = TaskForm(data={
            "title": None,
            "description": "test1123@test.com",
            "due_date": "2025-03-30"})
        self.assertFalse(form.is_valid())

    def test_false_date(self):
        form = TaskForm(data={
            "title": "test",
            "description": "test1123@test.com",
            "due_date": "2025-03-28"})
        self.assertFalse(form.is_valid())




class TestTaskAPI(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            username="tes123t111211233name",
            email="123t21131123est@123test.com",
            password="testpassword"
        )

    def test_positive_create(self):
        data = {
            "title": "1test1",
            "description": "test1123@test.com",
            "due_date": "2025-03-30"
        }
        credentials = "tes123t111211233name:testpassword"
        encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')

        response = self.client.post(
            "/api/tasks/",
            json.dumps(data),
            content_type="application/json",
            HTTP_AUTHORIZATION=f'Basic {encoded_credentials}'
        )
        self.assertEqual(response.status_code, 201)

    def test_negative_create(self):
        data = {
            "title": "testtesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttest",
            "description": "test1123@test.com",
            "due_date": "2025-03-30"
        }
        credentials = "tes123t111211233name:testpassword"
        encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')

        response = self.client.post(
            "/api/tasks/",
            json.dumps(data),
            content_type="application/json",
            HTTP_AUTHORIZATION=f'Basic {encoded_credentials}'
        )
        self.assertRaises(ValidationError)

    def test_description_none(self):
        data = {
            "title": "testtesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttest",
            "description": None,
            "due_date": "2025-03-30"
        }
        credentials = "tes123t111211233name:testpassword"
        encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')

        response = self.client.post(
            "/api/tasks/",
            json.dumps(data),
            content_type="application/json",
            HTTP_AUTHORIZATION=f'Basic {encoded_credentials}'
        )
        self.assertRaises(ValidationError)

    def test_false_due_date(self):
        data = {
            "title": "testtesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttest",
            "description": None,
            "due_date": "2025-03-28"
        }
        credentials = "tes123t111211233name:testpassword"
        encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')

        response = self.client.post(
            "/api/tasks/",
            json.dumps(data),
            content_type="application/json",
            HTTP_AUTHORIZATION=f'Basic {encoded_credentials}'
        )
        self.assertRaises(ValidationError)

class TestUserAPI(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            username="tes123t111211233name",
            email="123t21131123est@123test.com",
            password="testpassword"
        )

    def test_users_list(self):
        credentials = "tes123t111211233name:testpassword"
        encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
        response = self.client.get(
            "/api/users/",
            HTTP_AUTHORIZATION=f'Basic {encoded_credentials}'
        )
        self.assertEqual(response.status_code, 200)
