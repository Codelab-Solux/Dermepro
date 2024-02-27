from django.urls import path, register_converter
from .views import *
from base.utils import HashIdConverter

register_converter(HashIdConverter, "hashid")

urlpatterns = [
    path('', chats, name='chats'),
    path('threads/', threads, name='threads'),
    path('threads/<hashid:pk>/', thread, name='thread'),
    path('contacts/', contacts, name='contacts'),
    path('groups/', groups, name='groups'),
]
