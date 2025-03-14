from django.urls import re_path, path

from pasteapp.consumers import PasteConsumer
from . import consumers

websocket_urlpatterns = [
    # re_path(r'ws/some_path/$', consumers.ChatConsumer.as_asgi()),
    path("ws/paste/", PasteConsumer.as_asgi()),
]
