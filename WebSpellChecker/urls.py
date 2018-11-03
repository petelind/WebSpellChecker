"""WebSpellChecker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from SpellChecker.views import welcome, home, model_form_upload

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', welcome, name='root'),
    path('welcome', welcome, name='welcome'),
    path('login', LoginView.as_view(template_name='login_form.html'), name='user_login'),
    path('logout', LogoutView.as_view(), name='user_logout'),
    path('home', home, name='home'),
    path('new', model_form_upload, name='new_submission')
]
