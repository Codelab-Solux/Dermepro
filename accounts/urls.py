from django.urls import path, register_converter
from . import views
from .views import *
from base.utils import HashIdConverter

register_converter(HashIdConverter, "hashid")

urlpatterns = [
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
    path('change_user_status/<hashid:pk>/',
         change_user_status, name='change_user_status'),
    path('times/managements/', time_mgt, name='time_mgt'),
    path('times/management/<hashid:pk>/',
         time_mgt_details, name='time_mgt_details'),
    path('times/manage/<hashid:pk>/',
         manage_time, name='manage_time'),
]


htmx_urls = [
    path('users/<hashid:pk>/', user, name='user'),
    path('users/<hashid:pk>/alt/', user_alt, name='user_alt'),
    path('users/filter/<str:pk>/', filter_users, name='filter_users'),
    path('users/list/<str:pk>/', users_list, name='users_list'),
    path('times/records/new/', new_time_record, name='new_time_record'),
    path('times/records/<hashid:pk>/', recent_moves, name='recent_moves'),
    path('times/records/<hashid:pk>/', time_records, name='time_records'),
    path('times/records/<hashid:pk>/',
         filter_time_records, name='filter_time_records'),
    path('times/records/<hashid:pk>/<int:day>/',
         daily_time_records, name='daily_time_records'),
    path('times/calendar/', calendar_times, name='calendar_times'),
    path('times/calendar/<hashid:pk>/<int:day>/',
         filter_calendar_times, name='filter_calendar_times'),

]

urlpatterns += htmx_urls
