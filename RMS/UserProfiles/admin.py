from django.contrib import admin
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from .models import UserCred, Residents, Roles, Staffs

def transition_to_resident_only(modeladmin, request, queryset):
    for staff in queryset:
        user = staff.user
        if hasattr(user, 'staffs'):
            user.staffs.delete()  # Remove the staff profile
        user.is_staff = False
        user.save()
    modeladmin.message_user(request, "Selected users have been transitioned to resident only.")

transition_to_resident_only.short_description = "Transition selected users to Resident Only"

def transition_to_staff(modeladmin, request, queryset):
    for resident in queryset:
        user = resident.user
        if not user.is_staff:
            user.is_staff = True
            user.save()
            # Create the Staff profile for the user
            Staffs.objects.create(
                user=user,
                role=Role.objects.first()  # Assign a default role; you might want to handle this differently
            )
    modeladmin.message_user(request, "Selected users have been transitioned to staff.")

transition_to_staff.short_description = "Transition selected users to Staff"


class UserCredAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'firstname', 'lastname', 'phone_number', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'firstname', 'lastname')
    list_filter = ('is_staff', 'is_active')

class ResidentsAdmin(admin.ModelAdmin):
    list_display = ('user', 'guardian_phone_number')
    search_fields = ('user__username', 'guardian_phone_number')
    list_filter = ('user__username',)
    ordering = ('id',)
    actions = [transition_to_staff]

class RolesAdmin(admin.ModelAdmin):
    list_display = ('name', 'abbreviation')
    search_fields = ('name', 'abbreviation')
    filter_horizontal = ('permissions',)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['permissions'].queryset = Permission.objects.all()
        return form

class StaffsAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    search_fields = ('user__username', 'role__name')
    list_filter = ('role',)
    ordering = ('id',)
    actions = [transition_to_resident_only]

admin.site.register(UserCred, UserCredAdmin)
admin.site.register(Residents, ResidentsAdmin)
admin.site.register(Roles, RolesAdmin)
admin.site.register(Staffs, StaffsAdmin)
