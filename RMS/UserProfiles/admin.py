# your_app_name/admin.py

from django.contrib import admin
from .models import UserCred, Resident, Staff

@admin.register(UserCred)
class UserCredAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'firstname', 'lastname', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'firstname', 'lastname')
    list_filter = ('is_staff', 'is_active')

@admin.register(Resident)
class ResidentAdmin(admin.ModelAdmin):
    list_display = ('user',) #'room_id'
    search_fields = ('user__username',)
    raw_id_fields = ('user',)  # Improves performance for large databases

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    search_fields = ('user__username', 'role')
