"""Module for Django app urls"""
from django.urls import path
from . import views

urlpatterns = ([
    path("", views.admin_stats)
])
