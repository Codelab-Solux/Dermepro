from django.urls import path, register_converter
from .views import *
from .utils import HashIdConverter

register_converter(HashIdConverter, "hashid")

urlpatterns = [
    # path('', home, name='home'),
]


htmx_urls =[
 
]

urlpatterns += htmx_urls