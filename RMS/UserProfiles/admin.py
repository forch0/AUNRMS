# your_app_name/admin.py

from django.contrib import admin
from .models import UserCred, Resident, Staff, Role

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
    list_display = ('user', 'get_role_name')  # display user and related role name
    search_fields = ('user__username', 'role__name')

    def get_role_name(self, obj):
        return obj.role.name

    get_role_name.short_description = 'Role'  # column header

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'abbreviation')  # display both name and abbreviation
    search_fields = ('name', 'abbreviation')

