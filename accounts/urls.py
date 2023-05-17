from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('signup/', signupView, name='signup'),
    path('login/', loginView, name='login'),
    path('logout/', logoutUser, name='logout'),
    path('users/', users, name='users'),
    path('users/<str:pk>/', user_profile, name='user_profile'),
    path('parameters/', views.AjaxRolesView.as_view(), name='ajax_params'),
    path('ajax/user_role/create/',
         views.AjaxCreateRole.as_view(), name='ajax_create'),
    path('ajax/user_role/update/',
         views.AjaxUpdateRole.as_view(), name='ajax_update'),
    path('ajax/user_role/delete/',
         views.AjaxDeleteRole.as_view(), name='ajax_delete'),
]
