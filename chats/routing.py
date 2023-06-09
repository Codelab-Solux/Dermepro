from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path(r'chats/<str:id>/', consumers.PrivateChatConsumer.as_asgi()),
    path(r'notify/', consumers.NotificationConsumer.as_asgi()),
]
