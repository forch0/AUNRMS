from django.contrib import admin
from .models import UserCred, Resident, Staff, Role

@admin.register(UserCred)
class UserCredAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'firstname', 'lastname', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'firstname', 'lastname')
    list_filter = ('is_staff', 'is_active')
    ordering = ('id',)  # Sort by ID in ascending order by default

@admin.register(Resident)
class ResidentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user',)
    search_fields = ('user__username',)
    raw_id_fields = ('user',)
    ordering = ('id',)  # Sort by ID in ascending order by default

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'get_role_name')
    search_fields = ('user__username', 'role__name')

    def get_role_name(self, obj):
        return obj.role.name

    get_role_name.short_description = 'Role'
    ordering = ('id',)  # Sort by ID in ascending order by default

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'abbreviation')
    search_fields = ('name', 'abbreviation')
    ordering = ('id',)  # Sort by ID in ascending order by default
