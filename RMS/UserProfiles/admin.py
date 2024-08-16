from django.contrib import admin
from .models import UserCred, Residents, Staffs, Roles

def transition_to_resident_only(modeladmin, request, queryset):
    for staff in queryset:
        user = staff.user
        if hasattr(user, 'staffs'):
            user.staffs.delete()  # Remove the staff profile
        user.is_staff = False
        user.save()
    modeladmin.message_user(request, "Selected users have been transitioned to resident only.")

# transition_to_resident_only.short_description = "Transition selected users to Resident Only"

# def transition_to_staff(modeladmin, request, queryset):
#     for resident in queryset:
#         user = resident.user
#         if not user.is_staff:
#             user.is_staff = True
#             user.save()
#             # Create the Staff profile for the user
#             Staffs.objects.create(
#                 user=user,
#                 role=Role.objects.first()  # Assign a default role; you might want to handle this differently
#             )
#     modeladmin.message_user(request, "Selected users have been transitioned to staff.")

# transition_to_staff.short_description = "Transition selected users to Staff"


# @admin.register(UserCred)
# class UserCredAdmin(admin.ModelAdmin):
#     list_display = ('id', 'username', 'email', 'firstname', 'lastname', 'phone_number', 'is_staff', 'is_active')
#     search_fields = ('username', 'email', 'firstname', 'lastname')
#     list_filter = ('is_staff', 'is_active')
#     ordering = ('id',)

# @admin.register(Residents)
# class ResidentAdmin(admin.ModelAdmin):
#     list_display = ('id', 'username', 'guardian_phone_number')
#     search_fields = ('user__username',)
#     raw_id_fields = ('user',)
#     ordering = ('id',)
#     actions = [transition_to_staff]

#     def username(self, obj):
#         return obj.user.username
#     username.short_description = 'Username'

@admin.register(Staffs)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'role_name')
    search_fields = ('user__username', 'role__name')
    raw_id_fields = ('user', 'role')
    ordering = ('id',)
    actions = [transition_to_resident_only]

    def username(self, obj):
        return obj.user.username
    username.short_description = 'Username'

    def role_name(self, obj):
        return obj.role.name
    role_name.short_description = 'Role'

@admin.register(Roles)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'abbreviation')
    search_fields = ('name', 'abbreviation')
    ordering = ('id',)