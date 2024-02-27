from django.urls import path, register_converter
from .views import *
from .utils import HashIdConverter

register_converter(HashIdConverter, "hashid")

urlpatterns = [
    path('', home, name='home'),
    path('notifications/', notifications, name='notifications'),
    path('notifications/<hashid:pk>/read',
         read_notification, name='read_notification'),
    # -------------------------------------------------------------------------------
    path('visits/', visits, name='visits'),
    path('visits/new/', create_visit, name='create_visit'),
    path('visits/list/', visit_list, name='visit_list'),
    path('visits/filter/', filter_visits, name='filter_visits'),
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
    path('reports/', reports, name='reports'),
]


htmx_urls =[
    # appointments -----------------------------------------------------------
    path('appointments/list/', appointment_list, name='appointment_list'),
    path('appointments/table/', appointments_table, name='appointments_table'),
    path('appointments/table/filter/', filter_appointments_table, name='filter_appointments_table'),
    path('appointments/filter/', filter_appointments, name='filter_appointments'),
    path('appointments/ongoing/', ongoing_appointments, name='ongoing_appointments'),
    path('appointments/pending/', pending_appointments, name='pending_appointments'),
    path('appointments/pending/vip/', pending_vips, name='pending_vips'),
    path('appointments/pending/new/', create_appointment, name='create_appointment'),
    path('appointments/<hashid:pk>/<hashid:kp>/edit_status', edit_appointment_status, name='edit_appointment_status'),
    path('appointments/<hashid:pk>/badge/', generate_appointment_badge, name='generate_appointment_badge'),
    path('appointments/<hashid:pk>/signature/', sign_appointment, name='sign_appointment'),
    
    # visits -----------------------------------------------------------
    # path('visits/add/', add_visit, name='add_visit'),
    path('visits/table/', visits_table, name='visits_table'),
    path('visits/ongoing/', ongoing_visits, name='ongoing_visits'),
    path('visits/pending/', pending_visits, name='pending_visits'),
    path('visits/table/filter/', filter_visits_table, name='filter_visits_table'),
    path('visits/<hashid:pk>/badge/', generate_visit_badge, name='generate_visit_badge'),
    path('visits/<hashid:pk>/signature/', sign_visit, name='sign_visit'),
    
    # users -----------------------------------------------------------
    path('users/table/', users_table, name='users_table'),
    path('users/table/filter/', filter_users_table, name='filter_users_table'),
]

urlpatterns += htmx_urls