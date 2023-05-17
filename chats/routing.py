from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path(r'chats/', consumers.ChatConsumer.as_asgi()),
    path(r'chats/<str:id>/', consumers.ChatConsumer.as_asgi()),
    path(r'ws/socket-server/username/',
         consumers.ChatConsumer.as_asgi()),
]
