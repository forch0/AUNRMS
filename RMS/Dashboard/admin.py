from django.contrib import admin
from django.urls import path
from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
# from .views import admin_dashboard


admin.site.site_header = "AUN Residence Management System"
admin.site.site_title = "AUN Residence Management System"
admin.site.index_title = "Welcome to AUN Residence Management System"
