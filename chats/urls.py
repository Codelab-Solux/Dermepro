from django.urls import path, register_converter
from .views import *
from base.utils import HashIdConverter

register_converter(HashIdConverter, "hashid")

urlpatterns = [
    path('', chats, name='chat'),
    path('<hashid:pk>/', chat_page, name='chat_page'),
]
