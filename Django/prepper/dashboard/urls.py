from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # This sets up /home URL
]
