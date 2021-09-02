"""
ASGI config for buzzer project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

# import os

# from django.core.asgi import get_asgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'buzzer.settings')

# application = get_asgi_application()


import os

from django.conf.urls import url
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator
from channels.auth import AuthMiddlewareStack

from host.consumers import PlayerConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    # Just HTTP for now. (We can add other protocols later.)
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                [
                    url(r'host/', PlayerConsumer.as_asgi()),    #(?P<room_code>\d+)
                    url(r'join/', PlayerConsumer.as_asgi()),    # (?P<room_code>\d+)/(?P<username>\D+)$
                ]
            )
        )
    )
})

# messages/