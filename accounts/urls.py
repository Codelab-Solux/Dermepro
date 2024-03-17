from django.urls import path, register_converter
from . import views
from .views import *
from base.utils import HashIdConverter

register_converter(HashIdConverter, "hashid")

urlpatterns = [
    path('signup/', signupView, name='signup'),
    path('login/', loginView, name='login'),
    path('logout/', logoutUser, name='logout'),
    path('users/', users, name='users'),
    path('users/new/', create_user, name='create_user'),
    path('users/occupied', occupied_users, name='occupied_users'),
    path('users/unavailable', unavailable_users, name='unavailable_users'),
    path('users/<hashid:pk>/delete', delete_user, name='delete_user'),
    path('users/<hashid:pk>/edit', edit_user, name='edit_user'),
    path('change_user_status/<hashid:pk>/', change_user_status, name='change_user_status'),
    path('fetch_user_status/', fetch_user_status, name='fetch_user_status'),
]


htmx_urls =[
    path('users/<hashid:pk>/', user, name='user'),
    path('users/filter', filter_users, name='filter_users'),
    path('users/list/', user_list, name='user_list'),

]

urlpatterns += htmx_urls