from django.urls import path

from .views import *

urlpatterns = [
    path('', chats, name='chats'),
    path('<str:pk>/', chat_box, name='chat_box'),
    path('delete_text/<str:pk>/', delete_text, name='delete_text'),
    path('create_thread/<str:pk>/', create_thread, name='create_thread'),
    path('<str:pk>/messages/', get_msgs, name='get_msgs'),
]
