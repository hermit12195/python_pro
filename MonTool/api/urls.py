from django.urls import path

from api.views import Signup, Login, AddServer, ListServers

urlpatterns=[
    path('signup/', Signup.as_view(), name="signup"),
    path("login/", Login.as_view(), name="login"),
    path("addserver/", AddServer.as_view(), name="addserver"),
    path("listservers/", ListServers.as_view(), name="listservers")
]