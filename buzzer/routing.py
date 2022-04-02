from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/(?P<user_type>\w+)/(?P<room_name>\w+)/(?P<username>.*)/$', consumers.PlayerConsumer.as_asgi()),
    # re_path(r'ws/player/(?P<room_name>\w+)/$', consumers.PlayerConsumer.as_asgi()),
]