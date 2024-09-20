from django.contrib import admin
from django import forms
from django.contrib.auth.models import Permission
from .models import UserCred, Residents, Roles, Staffs
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

# def transition_to_resident_only(modeladmin, request, queryset):
#     for staff in queryset:
#         user = staff.user
#         if hasattr(user, 'staff_profile'):  # Corrected related_name
#             user.staff_profile.delete()  # Remove the staff profile
#         user.is_staff = False
#         user.save()
#     modeladmin.message_user(request, "Selected users have been transitioned to resident only.")

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
#                 role=Roles.objects.first()  # Assign a default role; adjust as needed
#             )
#     modeladmin.message_user(request, "Selected users have been transitioned to staff.")

# transition_to_staff.short_description = "Transition selected users to Staff"

# class UserCredAdmin(admin.ModelAdmin):
#     model = UserCred
#     fieldsets = (
#         (None, {'fields': ('email', 'password')}),
#         ('Personal info', {'fields': ('firstname', 'lastname', 'phone_number')}),
#         ('Permissions', {'fields': ('is_active', 'is_staff')}),


#     )
    
#     list_display = ('email', 'firstname', 'lastname', 'phone_number', 'is_staff', 'is_active')
#     search_fields = ('email', 'firstname', 'lastname')
#     list_filter = ('is_staff', 'is_active')
#     ordering = ('email',)

#     # readonly_fields = ('email',)  # Example of making the email field read-only

#     def get_changeform_initial_data(self, request):
#         """
#         Return the initial data to be used when rendering the form for changing a user's password.
#         """
#         user = self.get_object(request, self.get_changeform_initial_data(request))
#         return {'password': user.password}


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
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('firstname', 'lastname', 'phone_number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff')}),
    )
    
    list_display = ('email', 'firstname', 'lastname', 'phone_number', 'is_staff', 'is_active')
    search_fields = ('email', 'firstname', 'lastname')
    list_filter = ('is_staff', 'is_active')
    ordering = ('email',)

class ResidentsAdmin(admin.ModelAdmin):
    list_display = ('user', 'guardian_phone_number')
    search_fields = ('user__email', 'guardian_phone_number')  # Updated to use 'user__email'
    list_filter = ('user__email',)  # Updated to use 'user__email'
    ordering = ('id',)
    # actions = [transition_to_staff]

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
    search_fields = ('user__email', 'role__name')  # Updated to use 'user__email'
    list_filter = ('role',)
    ordering = ('id',)
    # actions = [transition_to_resident_only]

admin.site.register(UserCred, UserCredAdmin)
admin.site.register(Residents, ResidentsAdmin)
admin.site.register(Roles, RolesAdmin)
admin.site.register(Staffs, StaffsAdmin)
