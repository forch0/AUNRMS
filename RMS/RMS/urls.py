"""
URL configuration for RMS project.

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
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.conf.urls import handler403
from django.shortcuts import render
# from .admin import custom_admin_index
# from .admin import custom_admin_site
from UserProfiles.views import *

def custom_403_view(request, exception=None):
    return render(request, '403.html', status=403)

handler403 = custom_403_view

# Rate-limit admin login attempts: 5 POST requests per minute
urlpatterns = [
    path('admin_tools_stats/', include('admin_tools_stats.urls')),
    path('', include('Home.urls')),  # Home app URLs
    path('users/', include('UserProfiles.urls')),  # User profiles URLs
    path('dorms/', include('Dorms.urls')),  # Dorms-related URLs
    path('dashboard/', include('Dashboard.urls')),  # Dashboard-related URLs
    path('year/', include('AcademicYear.urls')), 
    path('admin/password_reset/', auth_views.PasswordResetView.as_view(), name='admin_password_reset'),
    path('admin/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='admin_password_reset_done'),
    path('admin/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='admin_password_reset_confirm'),
    path('admin/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='admin_password_reset_complete'),
    path('admin/', admin.site.urls),  # Admin path remains intact
    # '''Custom'''
    path('profile/', profile_information, name='profile_information'),
     path('past_enrollments/', past_enrollments,  name='past_enrollments'),
    path('past_staff_assignments/', past_staff_assignments,  name='past_staff_assignments'),
     # Academic year-related URLs
    # path('operations/', include('Actions.urls')),  # Actions-related URLs
]