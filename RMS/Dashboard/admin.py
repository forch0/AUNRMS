from django.contrib import admin

# Register your models here.


# class StaffAdmin(admin.ModelAdmin):
#     def has_module_permission(self, request):
#         # Only allow users with 'Staff' role to see this model in the admin
#         return request.user.groups.filter(name='Staff').exists()

#     def has_view_permission(self, request, obj=None):
#         # Check if the user has permission to view this specific object
#         return request.user.groups.filter(name='Staff').exists()


# class MyCustomModelAdmin(admin.ModelAdmin):
#     def get_queryset(self, request):
#         qs = super().get_queryset(request)
#         if request.user.groups.filter(name='Admin').exists():
#             return qs  # Admin can see all records
#         elif request.user.groups.filter(name='Manager').exists():
#             return qs.filter(assigned_to_manager=True)  # Manager can only see their records
#         return qs.none()  # Default: no records if the user doesn't match a role


# from .models import Roles, SomeSensitiveModel
# class SomeSensitiveModelAdmin(admin.ModelAdmin):
#     def has_module_permission(self, request):
#         # Allow users with the 'Admin' or 'Manager' role to see this model
#         allowed_roles = ['Admin', 'Manager']
#         if request.user.role and request.user.role.name in allowed_roles:
#             return True
#         return False

#     def has_view_permission(self, request, obj=None):
#         # Allow users with the 'Admin' or 'Manager' role to view this model
#         allowed_roles = ['Admin', 'Manager']
#         return request.user.role and request.user.role.name in allowed_roles


# if request.user.role and request.user.role.name == 'Admin':
#     admin.site.register(SomeSensitiveModel, SomeSensitiveModelAdmin)

# class SensitiveModelAdmin(admin.ModelAdmin):
#     def has_module_permission(self, request):
#         # Check if the user has the 'Admin' or 'Residence Director' role
#         allowed_roles = ['Admin', 'Residence Director']
#         return request.user.role and request.user.role.name in allowed_roles

#     def has_view_permission(self, request, obj=None):
#         # Allow viewing only for users with the allowed roles
#         allowed_roles = ['Admin', 'Residence Director']
#         return request.user.role and request.user.role.name in allowed_roles

#     def has_change_permission(self, request, obj=None):
#         # Allow changing only for users with the allowed roles
#         allowed_roles = ['Admin', 'Residence Director']
#         return request.user.role and request.user.role.name in allowed_roles

# admin.site.register(SensitiveModel, SensitiveModelAdmin)

# ----

# If you want to hide certain models from being listed on the admin dashboard for users without specific roles, you can customize the AdminSite.
# class MyAdminSite(AdminSite):
#     def has_permission(self, request):
#         # Restrict the entire admin interface to users with specific roles
#         allowed_roles = ['Admin', 'Residence Director']
#         return request.user.is_active and request.user.role and request.user.role.name in allowed_roles




# from django.contrib import admin
# from .models import MaintenanceRequest
# class MaintenanceRequestAdmin(admin.ModelAdmin):
#     def has_view_permission(self, request, obj=None):
#         # Allow only specific roles to view the list of maintenance requests
#         allowed_roles = ['Residence Assistant', 'Residence Director']
#         return request.user.role and request.user.role.name in allowed_roles

#     def has_add_permission(self, request):
#         # Allow only Residence Assistants and Directors to create new requests
#         allowed_roles = ['Residence Assistant', 'Residence Director']
#         return request.user.role and request.user.role.name in allowed_roles

#     def has_change_permission(self, request, obj=None):
#         # Allow only Residence Directors to edit requests
#         return request.user.role and request.user.role.name == 'Residence Director'

#     def has_delete_permission(self, request, obj=None):
#         # Allow only Admins to delete requests
#         return request.user.role and request.user.role.name == 'Admin'

# admin.site.register(MaintenanceRequest, MaintenanceRequestAdmin)


# ---------------------------
# class RoleBasedAdminMixin(admin.ModelAdmin):
#     allowed_roles = []

#     def has_view_permission(self, request, obj=None):
#         return request.user.role and request.user.role.name in self.allowed_roles

#     def has_add_permission(self, request):
#         return request.user.role and request.user.role.name in self.allowed_roles

#     def has_change_permission(self, request, obj=None):
#         return request.user.role and request.user.role.name in self.allowed_roles

#     def has_delete_permission(self, request, obj=None):
#         return request.user.role and request.user.role.name in self.allowed_roles


# class MaintenanceRequestAdmin(RoleBasedAdminMixin, admin.ModelAdmin):
#     allowed_roles = ['Residence Director', 'Admin']

# admin.site.register(MaintenanceRequest, MaintenanceRequestAdmin)
# ----------------------------------------

# custom_admin.py
# from django.contrib.admin import AdminSite
# from .models import Roles

# class RoleBasedAdminSite(AdminSite):
#     def get_model_perms(self, request, model):
#         """
#         Override this method to filter models based on user roles.
#         """
#         # Get the user's role
#         user_role = request.user.role.name if request.user.role else None

#         # Define model visibility for different roles
#         model_visibility = {
#             'Admin': ['MaintenanceRequest', 'Announcement', 'UserCred', 'Roles'],
#             'Residence Director': ['MaintenanceRequest', 'Announcement'],
#             'Residence Assistant': ['Announcement'],
#         }

#         # Show all models to superusers
#         if request.user.is_superuser:
#             return super().get_model_perms(request)

#         # Hide models not allowed for the user's role
#         if user_role in model_visibility:
#             if model._meta.model_name in [m.lower() for m in model_visibility[user_role]]:
#                 return super().get_model_perms(request)

#         return {'add': False, 'change': False, 'delete': False}

#     def has_permission(self, request):
#         return request.user.is_active and request.user.is_authenticated

# # Instantiate the custom admin site
# custom_admin_site = RoleBasedAdminSite(name='custom_admin')





admin.site.site_header = "AUN Residence Management System"
admin.site.site_title = "AUN Residence Management System"
admin.site.index_title = "Welcome to AUN Residence Management System"
