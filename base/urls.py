from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('', home, name='home'),
    path('notifications/', notifications, name='notifications'),
    path('notifications/<str:pk>/read',
         read_notification, name='read_notification'),
    path('visits/', visits, name='visits'),
    path('visits/new/', create_visit, name='create_visit'),
    path('visits/<str:pk>/', visit, name='visit'),
    path('delete_visit/<str:pk>/', delete_visit, name='delete_visit'),
    path('visit_csv', visit_csv, name='visit_csv'),
    path('appointments/', appointments, name='appointments'),
    path('appointments/new/', create_appointment, name='create_appointment'),
    path('appointments/<str:pk>/', appointment, name='appointment'),
    path('appointments_csv', appointments_csv, name='appointments_csv'),
    path('delete_appointments/<str:pk>/',
         delete_appointment, name='delete_appointment'),
    path('dashboard/', dashboard, name='dashboard'),
    path('parameters/', parameters, name='parameters'),
    path('parameters/roles/<str:pk>/', role, name='role'),
    path('parameters/delete_role/<str:pk>/', delete_role, name='delete_role'),
    path('about/', about, name='about'),
]
