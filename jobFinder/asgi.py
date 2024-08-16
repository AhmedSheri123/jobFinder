"""
ASGI config for jobFinder project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jobFinder.settings')

application = get_asgi_application()

from messenger import routing as messenger_routing
from notifications import routing as notifications_routing

application = ProtocolTypeRouter(
    {
        'http':get_asgi_application(),
        'websocket':AuthMiddlewareStack(
            URLRouter(
                messenger_routing.websocket_urlpatterns + notifications_routing.websocket_urlpatterns
            )
        )
    }
)
