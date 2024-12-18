"""
URL configuration for prepper project.

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
from accounts import views as aviews
from django.conf import settings
from django.conf.urls.static import static
from assessments import views as asviews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', aviews.registerOrLogin),
    path('register/', aviews.register, name = "register"),
    path('login/', aviews.user_login, name = "login"),
    path('home/', include('dashboard.urls')),
    path('random/', asviews.view_questions, name = "random"),
    # path('submit_answers/', asviews.submit_answers, name='submit_answers'),
    path('mistraltest/', asviews.mistral_test_view, name='mistral_test'),
]

if settings.DEBUG: 
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # This line tells Django to serve media files like images, videos, and documents
    # from the file system to the browser during development. It uses the settings 
    # MEDIA_URL to determine the URL path (e.g., /media/) and MEDIA_ROOT to determine
    # where on the local file system the files are stored.
    # It uses MEDIA_URL for the web address (e.g., /media/) and MEDIA_ROOT for where the files are saved on your computer.

#migzm
#GOMEZ2006