from django.urls import path, register_converter
from .views import *
from . import views
from .utils import HashIdConverter

register_converter(HashIdConverter, "hashid")

urlpatterns = [
    path('', home, name='home'),
    path('notifications/', notifications, name='notifications'),
    path('notifications/<hashid:pk>/read',
         read_notification, name='read_notification'),
    # -------------------------------------------------------------------------------
    path('filter_visits/', filter_visits, name='filter_visits'),
    path('visit_list/', visit_list, name='visit_list'),
    path('visits/', visits, name='visits'),
    path('visits/new/', create_visit, name='create_visit'),
    path('visits/<hashid:pk>/', visit, name='visit'),
    path('visits/<hashid:pk>/edit', edit_visit, name='edit_visit'),
    path('visits/<hashid:pk>/delete', delete_visit, name='delete_visit'),
    path('visits/<hashid:pk>/<hashid:kp>/edit_status', edit_visit_status, name='edit_visit_status'),
    path('visit_csv', visit_csv, name='visit_csv'),
    # -------------------------------------------------------------------------------
    path('appointments/', appointments, name='appointments'),
    path('appointments/new/', create_appointment, name='create_appointment'),
    path('appointments/<hashid:pk>/', appointment, name='appointment'),
    path('appointments/<hashid:pk>/edit', edit_appointment, name='edit_appointment'),
    path('appointments_csv', appointments_csv, name='appointments_csv'),
    path('delete_appointments/<hashid:pk>/',
         delete_appointment, name='delete_appointment'),
    path('dashboard/', dashboard, name='dashboard'),
    path('parameters/', parameters, name='parameters'),
    path('parameters/roles/<hashid:pk>/', role, name='role'),
    path('parameters/delete_role/<hashid:pk>/', delete_role, name='delete_role'),
    path('about/', about, name='about'),
]


htmx_urls =[
    # appointments -----------------------------------------------------------
    path('appointments/ongoing/', ongoing_appointments, name='ongoing_appointments'),
    path('appointments/pending/', pending_appointments, name='pending_appointments'),
    path('appointments/pending/vip/', pending_vips, name='pending_vips'),
    path('appointments/pending/new/', create_appointment, name='create_appointment'),
    path('appointment_list/', appointment_list, name='appointment_list'),
    path('appointments/<hashid:pk>/<hashid:kp>/edit_status', edit_appointment_status, name='edit_appointment_status'),
    path('filter_appointments/', filter_appointments, name='filter_appointments'),
    
    # visits -----------------------------------------------------------
    # path('visits/add/', add_visit, name='add_visit'),
    path('visits/ongoing/', ongoing_visits, name='ongoing_visits'),
    path('visits/pending/', pending_visits, name='pending_visits'),
]

urlpatterns += htmx_urls