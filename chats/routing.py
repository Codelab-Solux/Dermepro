from django.urls import path, register_converter
from . import consumers
from base.utils import HashIdConverter

register_converter(HashIdConverter, "hashid")

websocket_urlpatterns = [
    path('ws/chats/threads/<int:id>/', consumers.PrivateChatConsumer.as_asgi()),
]
