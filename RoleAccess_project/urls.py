"""
URL configuration for RoleAccess_project project.

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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from RoleAccess_app.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingPage, name='landing_page'),
    path('login-signup/', UserLogin, name='user_login'),
    path('login-signup/sign-up/', UserSignup, name='user_signup'),
    path('register/', UserRegister, name='user_register'),
    path('doctor/', DoctorPage, name='doctor'),
    path('doctor/blog/', UploadBlog, name='doctor_blog'),
    path('patient/', PatientPage, name='patient'),
    path('check-username-email/', CheckValidUser, name="check_username_email"),
    

    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
