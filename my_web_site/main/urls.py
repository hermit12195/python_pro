from django.urls import path
from . import views

urlpatterns=[
    path("", views.home),
    path("about/", views.about),
    path("contacts/", views.ContactView.as_view()),
    path("services/", views.ServiceView.as_view()),
    path("search/", views.search, name="search")
]