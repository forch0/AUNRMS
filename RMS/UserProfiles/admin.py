from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django import forms
from .models import UserCred, Residents, Staffs, Roles
from django.utils.translation import gettext as _

# Custom form for UserCred Admin
class UserCredAdminForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:  
        model = UserCred
        fields = ('email', 'firstname', 'lastname', 'phone_number', 'is_active', 'is_staff')

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data['password']:
            user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class UserAdmin(BaseUserAdmin):
    form = UserCredAdminForm  # Use the custom form for user management
    list_display = ('email', 'firstname', 'lastname', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('email', 'firstname', 'lastname')
    ordering = ('email',)

    # Remove permissions section from user admin
    fieldsets = (
        (None, {'fields': ('email', 'firstname', 'lastname', 'phone_number', 'is_staff', 'is_active', 'is_superuser', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {'fields': ('email', 'firstname', 'lastname', 'phone_number', 'is_staff', 'is_active', 'is_superuser', 'password')}), 
    )

class RolesAdmin(admin.ModelAdmin):
    list_display = ('name', 'abbreviation')
    search_fields = ('name', 'abbreviation')
    filter_horizontal = ('permissions',)  # Use horizontal filter for permissions

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        # Create or update the group associated with this role
        group, created = Group.objects.get_or_create(name=obj.name)

        # Clear existing permissions before assigning new ones
        group.permissions.clear()
        group.permissions.set(obj.permissions.all())
        group.save()

        # Provide feedback to the admin
        if created:
            self.message_user(request, _("Group created: %s") % group.name, level='success')
        else:
            self.message_user(request, _("Group updated: %s") % group.name, level='info')

class ResidentsAdmin(admin.ModelAdmin):
    list_display = ('user', 'guardian_phone_number', 'address', 'role')
    search_fields = ('user__email', 'guardian_phone_number', 'address')
    list_filter = ('role',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Dynamically filter based on user permissions
        if request.user.is_superuser:
            return qs
        return qs.filter(role__permissions__user=request.user)

class StaffsAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'date_joined')
    search_fields = ('user__email', 'role__name')
    list_filter = ('role',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Dynamically filter based on user permissions
        if request.user.is_superuser:
            return qs
        return qs.filter(role__permissions__user=request.user)

# Unregister the default Group admin
admin.site.unregister(Group)

# Register models with the admin site
admin.site.register(UserCred, UserAdmin)
admin.site.register(Roles, RolesAdmin)
admin.site.register(Residents, ResidentsAdmin)
admin.site.register(Staffs, StaffsAdmin)
