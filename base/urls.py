from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('', home, name='home'),
    path('visits/', visits, name='visits'),
    path('visits/<str:pk>/', visit_detail, name='visit_detail'),
    path('delete_visit/<str:pk>/', delete_visit, name='delete_visit'),
    path('visit_csv', visit_csv, name='visit_csv'),
    path('appointments/', appointments, name='appointments'),
    path('appointments/<str:pk>/', appointment_detail, name='appointment_detail'),
    path('rdv_csv', rdv_csv, name='rdv_csv'),
    path('delete_rdv/<str:pk>/', delete_rdv, name='delete_rdv'),
    path('dashboard/', dashboard, name='dashboard'),
    path('parameters/', parameters, name='parameters'),
    path('parameters/roles/<str:pk>/', role_detail, name='role_detail'),
    path('parameters/delete_role/<str:pk>/', delete_role, name='delete_role'),
    path('about/', about, name='about'),
]
