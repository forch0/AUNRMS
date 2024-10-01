from django.contrib import admin
from django import forms
from django.contrib.auth.models import Permission
from .models import UserCred, Residents, Roles, Staffs
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

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

class UserCredAdmin(admin.ModelAdmin):
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
# Residents Admin configuration
class ResidentsAdmin(admin.ModelAdmin):
    list_display = ('user', 'guardian_phone_number')
    search_fields = ('user__email', 'guardian_phone_number')
    list_filter = ('user__email',)
    ordering = ('id',)

# Roles Admin configuration
class RolesAdmin(admin.ModelAdmin):
    list_display = ('name', 'abbreviation')
    search_fields = ('name', 'abbreviation')
    filter_horizontal = ('permissions',)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Ensure all permissions are available in the admin interface
        form.base_fields['permissions'].queryset = Permission.objects.all()
        return form

# Staffs Admin configuration
class StaffsAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    search_fields = ('user__email', 'role__name')
    list_filter = ('role',)
    ordering = ('id',)

# Register models with the admin site
admin.site.register(UserCred, UserCredAdmin)
admin.site.register(Residents, ResidentsAdmin)
admin.site.register(Roles, RolesAdmin)
admin.site.register(Staffs, StaffsAdmin)
