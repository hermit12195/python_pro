from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.serializers import SignupSerializer, LoginSerializer, AddServerSerializer, ListServersSerializer
from app.models import Server


class AuthMixin(CreateAPIView):
    def perform_create(self, serializer):
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        self.token = token

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response(data={"token": self.token.key}, status=self.status)


class Signup(AuthMixin):
    serializer_class = SignupSerializer
    status=status.HTTP_201_CREATED


class Login(AuthMixin):
    serializer_class = LoginSerializer
    status = status.HTTP_200_OK

class AddServer(CreateAPIView):
    serializer_class = AddServerSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ListServers(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ListServersSerializer

    def get_queryset(self):
        return Server.objects.filter(owner=self.request.user)


