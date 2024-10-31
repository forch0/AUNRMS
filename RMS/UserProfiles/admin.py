from django.contrib import admin
from django import forms
from .forms import ResidentsForm, StaffForm
from django.contrib.auth.models import Permission
from .models import UserCred, Residents, Roles, Staffs
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext as _
from adminsortable2.admin import SortableAdminMixin
from typing import Any
from django.http import HttpRequest

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
class UserAdmin(admin.ModelAdmin):
    form = UserCredAdminForm
    fieldsets = (
        (None, {'fields': ('email', 'password')}),  # Ensure 'username' is not here
        ('Personal info', {'fields': ('firstname', 'lastname', 'phone_number', 'date_joined')}),
        ('Permissions', {'fields': ('is_active', 'is_staff')}),
    )
    
    list_display = ('email', 'firstname', 'lastname', 'phone_number', 'date_joined', 'is_staff', 'is_active')
    search_fields = ('email', 'firstname', 'lastname')
    list_filter = ('is_staff', 'is_active')
    ordering = ('email',)

    def _is_superuser(self, request: HttpRequest) -> bool:
        """Checks if the user is a Django superuser."""
        return request.user.is_superuser
    
    def _has_selected_roles(self, request: HttpRequest) -> bool:
        """Checks if the user has one of the allowed roles."""
        allowed_roles = ['ResLife Directors',]  # Add the role names you want here
        staff = Staffs.objects.filter(user=request.user).first()
        if staff:
            return staff.role.name in allowed_roles
        return False
    
    def has_view_permission(self, request: HttpRequest, obj: Any | None = None) -> bool:
        """Allows selected roles and superuser to view the model."""
        return self._is_superuser(request) or self._has_selected_roles(request)

    def has_add_permission(self, request: HttpRequest) -> bool:
        """Only superuser can add."""
        return self._is_superuser(request)

    def has_change_permission(self, request: HttpRequest, obj: Any | None = None) -> bool:
        """Only superuser can change."""
        return self._is_superuser(request)

    def has_delete_permission(self, request: HttpRequest, obj: Any | None = None) -> bool:
        """Only superuser can delete."""
        return self._is_superuser(request)
class RolesAdmin(SortableAdminMixin,admin.ModelAdmin):
    list_display = ('name', 'abbreviation','my_order')
    search_fields = ('name', 'abbreviation')
    filter_horizontal = ('permissions',)
    ordering = ['my_order']  # Use horizontal filter for permissions


    def change_view(self, request, object_id, form_url='', extra_context=None):
        # Load custom CSS
        extra_context = extra_context or {}
        extra_context['custom_css'] = 'css/admin_custom.css'
        return super().change_view(request, object_id, form_url, extra_context=extra_context)
    
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

        def _is_superuser(self, request: HttpRequest) -> bool:
            """Checks if the user is a Django superuser."""
        return request.user.is_superuser
    
    def _is_superuser(self, request: HttpRequest) -> bool:
        """Checks if the user is a Django superuser."""
        return request.user.is_superuser
    
    def _has_selected_roles(self, request: HttpRequest) -> bool:
        """Checks if the user has one of the allowed roles."""
        allowed_roles = ['ResLife Directors',]  # Add the role names you want here
        staff = Staffs.objects.filter(user=request.user).first()
        if staff:
            return staff.role.name in allowed_roles
        return False
    
    def has_view_permission(self, request: HttpRequest, obj: Any | None = None) -> bool:
        """Allows selected roles and superuser to view the model."""
        return self._is_superuser(request) or self._has_selected_roles(request)

    def has_add_permission(self, request: HttpRequest) -> bool:
        """Only superuser can add."""
        return self._is_superuser(request)

    def has_change_permission(self, request: HttpRequest, obj: Any | None = None) -> bool:
        """Only superuser can change."""
        return self._is_superuser(request)

    def has_delete_permission(self, request: HttpRequest, obj: Any | None = None) -> bool:
        """Only superuser can delete."""
        return self._is_superuser(request)
class ResidentsAdmin(admin.ModelAdmin):
    form = ResidentsForm
    list_display = ('user', 'guardian_phone_number', 'address', 'role')
    search_fields = ('user__email', 'guardian_phone_number', 'address')
    list_filter = ('role',)
    autocomplete_fields = ['user']

    def _is_superuser(self, request: HttpRequest) -> bool:
        """Checks if the user is a Django superuser."""
        return request.user.is_superuser
    
    def _has_selected_roles(self, request: HttpRequest) -> bool:
        """Checks if the user has one of the allowed roles."""
        allowed_roles = ['ResLife Directors',]  # Add the role names you want here
        staff = Staffs.objects.filter(user=request.user).first()
        if staff:
            return staff.role.name in allowed_roles
        return False
    
    def has_view_permission(self, request: HttpRequest, obj: Any | None = None) -> bool:
        """Allows selected roles and superuser to view the model."""
        return self._is_superuser(request) or self._has_selected_roles(request)

    def has_add_permission(self, request: HttpRequest) -> bool:
        """Only superuser can add."""
        return self._is_superuser(request)

    def has_change_permission(self, request: HttpRequest, obj: Any | None = None) -> bool:
        """Only superuser can change."""
        return self._is_superuser(request)

    def has_delete_permission(self, request: HttpRequest, obj: Any | None = None) -> bool:
        """Only superuser can delete."""
        return self._is_superuser(request)

class StaffsAdmin(admin.ModelAdmin):
    form = StaffForm
    list_display = ('user', 'role', 'date_joined')
    search_fields = ('user__email', 'role__name')
    list_filter = ('role',)
    autocomplete_fields = ['user']

    def _is_superuser(self, request: HttpRequest) -> bool:
        """Checks if the user is a Django superuser."""
        return request.user.is_superuser
    
    def _has_selected_roles(self, request: HttpRequest) -> bool:
        """Checks if the user has one of the allowed roles."""
        allowed_roles = ['ResLife Directors',]  # Add the role names you want here
        staff = Staffs.objects.filter(user=request.user).first()
        if staff:
            return staff.role.name in allowed_roles
        return False
    
    def has_view_permission(self, request: HttpRequest, obj: Any | None = None) -> bool:
        """Allows selected roles and superuser to view the model."""
        return self._is_superuser(request) or self._has_selected_roles(request)

    def has_add_permission(self, request: HttpRequest) -> bool:
        """Only superuser can add."""
        return self._is_superuser(request)

    def has_change_permission(self, request: HttpRequest, obj: Any | None = None) -> bool:
        """Only superuser can change."""
        return self._is_superuser(request)

    def has_delete_permission(self, request: HttpRequest, obj: Any | None = None) -> bool:
        """Only superuser can delete."""
        return self._is_superuser(request)
    # def get_queryset(self, request):
    #     qs = super().get_queryset(request)
    #     # Dynamically filter based on user permissions
    #     if request.user.is_superuser or self._has_selected_roles(request):
    #         return qs
    #     return qs.filter(role__permissions__user=request.user)

# Unregister the default Group admin
admin.site.unregister(Group)
admin.site.register(UserCred, UserAdmin)
admin.site.register(Roles, RolesAdmin)
admin.site.register(Residents, ResidentsAdmin)
admin.site.register(Staffs, StaffsAdmin)
