"""URLs module"""
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views


urlpatterns = [
    path("", views.register_view),
    path("profile/<str:username>", views.profile_view, name="profile_view"),
    path('profile/edit/<str:username>', views.edit_profile, name="edit_profile"),
    path('profile/changepass/<str:username>', views.change_pass, name="change_pass")
]
