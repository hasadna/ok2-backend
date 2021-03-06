"""ok2_backend URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from django.urls import include, path

from one_minute_speeches.views import one_minute_speeches
from accounts.views import login, registration_view

api_patterns = [
    path('admin', admin.site.urls),
    path('login', login),
    path('register', registration_view),
    path('one_minute_speeches', one_minute_speeches),
]

urlpatterns = [path('api/', include(api_patterns))]
