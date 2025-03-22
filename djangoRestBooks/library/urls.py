"""URLs Module"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('books', views.BookView, basename="book")

urlpatterns = [
    path("api/", include(router.urls)),
    path('books/<int:pk>', views.BookDetails.as_view())
]
