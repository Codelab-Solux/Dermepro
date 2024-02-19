from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('chats/<str:id>/', consumers.PrivateChatConsumer.as_asgi()),
]
