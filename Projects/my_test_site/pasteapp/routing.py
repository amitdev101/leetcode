from django.urls import path
from .consumers import PasteConsumer

websocket_urlpatterns = [
    path("ws/paste/", PasteConsumer.as_asgi()),
]
