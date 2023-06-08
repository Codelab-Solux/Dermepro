from django.urls import path
from .views import *

urlpatterns = [
    path('', chats, name='chat'),
    path('<str:pk>/', chat_page, name='chat_page'),
]
