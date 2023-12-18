from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('chats/<str:id>/', consumers.PrivateChatConsumer.as_asgi()),
    path('notify/', consumers.NotificationConsumer.as_asgi()),
]
