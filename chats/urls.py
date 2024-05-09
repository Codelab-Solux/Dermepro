from django.urls import path, register_converter
from .views import *
from base.utils import HashIdConverter

register_converter(HashIdConverter, "hashid")

urlpatterns = [
    path('', chats, name='chats'),
    path('threads/', threads, name='threads'),
    path('threads/filter/', filter_threads, name='filter_threads'),
    path('threads/<hashid:pk>/', thread, name='thread'),
    path('contacts/', contacts, name='contacts'),
    path('contacts/filter/', filter_contacts, name='filter_contacts'),
    path('groups/', groups, name='groups'),
]
