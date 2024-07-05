from django.contrib import admin
from .models import UserCred, Residents, Staffs, Roles

@admin.register(UserCred)
class UserCredAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'firstname', 'lastname', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'firstname', 'lastname')
    list_filter = ('is_staff', 'is_active')
    ordering = ('id',)
# , 'uuid'
@admin.register(Residents)
class ResidentAdmin(admin.ModelAdmin):
    list_display = ('id', 'uuid', 'username',)
    search_fields = ('user__username',)
    raw_id_fields = ('user',)
    ordering = ('id',)

    def username(self, obj):
        return obj.user.username
    username.short_description = 'Username'

@admin.register(Staffs)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('id', 'uuid', 'username', 'role_name')
    search_fields = ('user__username', 'role__name')
    ordering = ('id',)

    def username(self, obj):
        return obj.user.username
    username.short_description = 'Username'

    def role_name(self, obj):
        return obj.role.name
    role_name.short_description = 'Role'

@admin.register(Roles)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'uuid', 'name', 'abbreviation')
    search_fields = ('name', 'abbreviation')
    ordering = ('id',)
