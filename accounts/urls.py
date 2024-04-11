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
    path('users/status_quo', users_status_quo, name='users_status_quo'),
    path('users/status_quo', users_status_quo, name='users_status_quo'),
    path('users/<hashid:pk>/profile', profile, name='profile'),
    path('users/<hashid:pk>/delete', delete_user, name='delete_user'),
    path('users/<hashid:pk>/edit', edit_user, name='edit_user'),
    path('profiles/<hashid:pk>/edit', edit_profile, name='edit_profile'),
    path('change_user_status/<hashid:pk>/', change_user_status, name='change_user_status'),
]


htmx_urls =[
    path('users/<hashid:pk>/', user, name='user'),
    path('users/filter', filter_users, name='filter_users'),
    path('users/list/', user_list, name='user_list'),

]

urlpatterns += htmx_urls