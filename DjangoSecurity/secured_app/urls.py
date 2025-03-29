from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


router=DefaultRouter()
router.register("tasks", views.TaskView, basename="tasks")
router.register("users", views.UserView, basename="users")
urlpatterns=[
    path("signup/", views.signup_view, name="signup"),
    path("", views.signin_view, name="signin"),
    path("logout/", views.logout_view, name="logout"),
    path("<str:username>/home/", views.home_view, name="home"),
    path("<str:username>/task/<str:title>", views.task_detail_view, name="task_detail"),
    path("api/", include(router.urls)),
]