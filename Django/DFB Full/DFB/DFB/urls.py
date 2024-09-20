"""
URL configuration for DFB project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include("DFBApp.urls")), # If a link has anything that ISNT "admin/" after the root (127.0.0.1), django goes to the urls.py file 
    #in DFBApp and only sends the link FOLLOWING THE ROOT (E.g: only v1/ is sent to urls.py if (root)/v1/ is typed) - (See urls.py in DFB for further explanation)
    path('admin/', admin.site.urls), # If a link has "admin/"" after the root (127.0.0.1/), the admin control panel is opened
    #Goes to the urls.py file that was defined in the DFBApp when http://127.0.0.1:8000/ or http://127.0.0.1:8000/xxxxx is typed
    
]
