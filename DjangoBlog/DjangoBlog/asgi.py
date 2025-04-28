"""
ASGI config for DjangoBlog project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

import django

django.setup()
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from chats.ws.urls import socket_urlpatterns


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoBlog.settings')

application  = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(
            URLRouter(socket_urlpatterns)
        )
    }
)
