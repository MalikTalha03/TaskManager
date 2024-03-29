"""
URL configuration for TaskManager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from task_manager import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.home, name='home'),
    path("login/", views.user_login, name='login'),
    path("dashboard/", views.dashboard, name='dashboard'),
    path("addtask/",views.addtask,name = 'add_task'),
    path('logout/', views.user_logout, name='logout'),
    path('update_task_status/', views.update_task_status, name='update_task_status'),
    path('update_password/', views.update_password, name='update_password'),
    path('my_profile/', views.my_profile, name='my_profile'),
    path('update_profile/', views.update_profile, name='update_profile'),
]

