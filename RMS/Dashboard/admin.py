# '''oLDEST'''
from django.contrib import admin
# from django.urls import path
# from django.contrib import admin
# from django.urls import path
# from django.shortcuts import redirect
# from django.contrib.auth import get_user_model
# from django.contrib.auth.models import Permission
# # from .views import admin_dashboard
admin.site.site_header = "AUN Residence Management System"
admin.site.site_title = "AUN Residence Management System"
admin.site.index_title = "Welcome to AUN Residence Management System"

'''working'''
# from django.contrib.admin import AdminSite
# from django.shortcuts import render
# from UserProfiles.models import UserCred, Residents, Staffs
# from AcademicYear.models import Enrollment, StaffAssignment
# class CustomAdminSite(AdminSite):
#     site_header = "AUN Residence Management System"
#     site_title = "AUN Residence Management System"
#     index_title = "Welcome to AUN Residence Management System"

#     def index(self, request, extra_context=None):
#         user = request.user  # Get logged-in user
#         context = {'role': None}  # Initialize context with no role

#         try:
#             # Fetch UserCred data
#             user_cred = UserCred.objects.get(email=user.email)

#             if user_cred.is_resident:
#                 # Fetch resident-specific data
#                 resident = Residents.objects.get(user=user_cred)
#                 current_enrollment = (
#                     Enrollment.objects.filter(resident=resident, status='active')
#                     .order_by('-date_enrolled')
#                     .first()
#                 )
#                 staff_assignments = (
#                     StaffAssignment.objects.filter(dorm=current_enrollment.dorm)
#                     if current_enrollment
#                     else []
#                 )
#                 context.update({
#                     'role': 'Resident',
#                     'user_data': resident,
#                     'current_enrollment': current_enrollment,
#                     'staff_assignments': staff_assignments,
#                 })

#             elif hasattr(user_cred, 'staffs'):
#                 # Fetch staff-specific data
#                 staff = Staffs.objects.get(user=user_cred)
#                 current_assignment = (
#                     StaffAssignment.objects.filter(staff=staff)
#                     .order_by('-created_at')
#                     .first()
#                 )
#                 context.update({
#                     'role': 'Staff',
#                     'user_data': staff,
#                     'current_assignment': current_assignment,
#                 })

#         except UserCred.DoesNotExist:
#             context['error'] = "User profile not found."
#         except Residents.DoesNotExist:
#             context['error'] = "Resident profile not found."
#         except Staffs.DoesNotExist:
#             context['error'] = "Staff profile not found."

#         # Render custom admin index page
#         return render(request, 'admin/index.html', context)
# # Register custom admin site
# custom_admin_site = CustomAdminSite(name='custom_admin')

'''working 2'''
# from django.contrib import admin
# from django.shortcuts import render
# from UserProfiles.models import UserCred, Residents, Staffs
# from AcademicYear.models import Enrollment, StaffAssignment
# class CustomAdminSite(admin.AdminSite):
#     site_header = "AUN Residence Management System"
#     site_title = "AUN Residence Management System"
#     index_title = "Welcome to AUN Residence Management System"

#     def index(self, request, extra_context=None):
#         # Custom content logic here
#         user = request.user
#         context = {'role': None}  # Default context with no role

#         try:
#             user_cred = UserCred.objects.get(email=user.email)

#             if user_cred.is_resident:
#                 resident = Residents.objects.get(user=user_cred)
#                 current_enrollment = (
#                     Enrollment.objects.filter(resident=resident, status='active')
#                     .order_by('-date_enrolled')
#                     .first()
#                 )
#                 staff_assignments = (
#                     StaffAssignment.objects.filter(dorm=current_enrollment.dorm)
#                     if current_enrollment
#                     else []
#                 )
#                 context.update({
#                     'role': 'Resident',
#                     'user_data': resident,
#                     'current_enrollment': current_enrollment,
#                     'staff_assignments': staff_assignments,
#                 })

#             elif hasattr(user_cred, 'staffs'):
#                 staff = Staffs.objects.get(user=user_cred)
#                 current_assignment = (
#                     StaffAssignment.objects.filter(staff=staff)
#                     .order_by('-created_at')
#                     .first()
#                 )
#                 context.update({
#                     'role': 'Staff',
#                     'user_data': staff,
#                     'current_assignment': current_assignment,
#                 })

#         except UserCred.DoesNotExist:
#             context['error'] = "User profile not found."
#         except Residents.DoesNotExist:
#             context['error'] = "Resident profile not found."
#         except Staffs.DoesNotExist:
#             context['error'] = "Staff profile not found."

#         return render(request, 'admin/index.html', context)
# # Register the custom admin site
# custom_admin_site = CustomAdminSite(name='custom_admin')


# from django.contrib import admin
# from django.shortcuts import render
# from UserProfiles.models import UserCred, Residents, Staffs
# from AcademicYear.models import Enrollment, StaffAssignment

# class CustomAdminSite(admin.AdminSite):
#     site_header = "AUN Residence Management System"
#     site_title = "AUN Residence Management System"
#     index_title = "Welcome to AUN Residence Management System"

#     def custom_dashboard(self, request):
#         user = request.user
#         context = {'role': None}  # Default context with no role

#         try:
#             user_cred = UserCred.objects.get(email=user.email)

#             if user_cred.is_resident:
#                 resident = Residents.objects.filter(user=user_cred).first()
#                 if resident:
#                     current_enrollment = (
#                         Enrollment.objects.filter(resident=resident, status='active')
#                         .order_by('-date_enrolled')
#                         .first()
#                     )
#                     staff_assignments = (
#                         StaffAssignment.objects.filter(dorm=current_enrollment.dorm)
#                         if current_enrollment
#                         else []
#                     )
#                     context.update({
#                         'role': 'Resident',
#                         'user_data': resident,
#                         'current_enrollment': current_enrollment,
#                         'staff_assignments': staff_assignments,
#                     })
#                 else:
#                     context['error'] = "Resident profile not found."

#             elif hasattr(user_cred, 'staffs'):
#                 staff = Staffs.objects.filter(user=user_cred).first()
#                 if staff:
#                     current_assignment = (
#                         StaffAssignment.objects.filter(staff=staff)
#                         .order_by('-created_at')
#                         .first()
#                     )
#                     context.update({
#                         'role': 'Staff',
#                         'user_data': staff,
#                         'current_assignment': current_assignment,
#                     })
#                 else:
#                     context['error'] = "Staff profile not found."

#             else:
#                 context['error'] = "No role assigned."

#         except UserCred.DoesNotExist:
#             context['error'] = f"User profile with email {user.email} not found."

#         return render(request, 'admin/custom_dashboard.html', context)

# custom_admin_site = CustomAdminSite(name='custom_admin')


'''2'''
# from django.contrib.admin.sites import site
# from django.shortcuts import render
# from UserProfiles.models import Residents, Staffs
# from AcademicYear.models import Enrollment, StaffAssignment

# def custom_admin_index(request, extra_context=None):
#     """
#     Overrides the default admin index page to include additional user-specific context.
#     """
#     user = request.user
#     context = {'role': None}  # Initialize context with no role

#     try:
#         # Check if the user is a resident or staff
#         user_cred = request.user

#         if hasattr(user_cred, 'residents'):
#             # Resident-specific data
#             resident = Residents.objects.get(user=user_cred)
#             current_enrollment = (
#                 Enrollment.objects.filter(resident=resident, status='active')
#                 .order_by('-date_enrolled')
#                 .first()
#             )
#             staff_assignments = (
#                 StaffAssignment.objects.filter(dorm=current_enrollment.dorm)
#                 if current_enrollment
#                 else []
#             )
#             context.update({
#                 'role': 'Resident',
#                 'user_data': resident,
#                 'current_enrollment': current_enrollment,
#                 'staff_assignments': staff_assignments,
#             })

#         elif hasattr(user_cred, 'staffs'):
#             # Staff-specific data
#             staff = Staffs.objects.get(user=user_cred)
#             current_assignment = (
#                 StaffAssignment.objects.filter(staff=staff)
#                 .order_by('-created_at')
#                 .first()
#             )
#             context.update({
#                 'role': 'Staff',
#                 'user_data': staff,
#                 'current_assignment': current_assignment,
#             })

#     except Residents.DoesNotExist:
#         context['error'] = "Resident profile not found."
#     except Staffs.DoesNotExist:
#         context['error'] = "Staff profile not found."

#     # Update the extra context for the default admin index template
#     extra_context = extra_context or {}
#     extra_context.update(context)

#     # Use the default admin site index view with the updated context
#     return site.index(request, extra_context=extra_context)


'''3'''
# from django.contrib.admin.sites import site
# from django.shortcuts import render
# from UserProfiles.models import UserCred, Residents, Staffs
# from AcademicYear.models import Enrollment, StaffAssignment

# def custom_admin_index(request, extra_context=None):
#     """
#     Custom admin index page to display user-specific data without disrupting the default admin.
#     """
#     user = request.user
#     context = {'role': None}  # Default context with no role

#     # Debugging: Ensure the user is authenticated
#     if not user.is_authenticated:
#         context['error'] = "User is not logged in."
#         return site.index(request, extra_context=extra_context)

#     try:
#         # Access the UserCred instance
#         user_cred = UserCred.objects.get(email=user.email)

#         if user_cred.is_resident:
#             # Fetch Resident-specific data
#             resident = user_cred.residents  # Related object from OneToOneField
#             current_enrollment = (
#                 Enrollment.objects.filter(resident=resident, status='active')
#                 .order_by('-date_enrolled')
#                 .first()
#             )
#             staff_assignments = (
#                 StaffAssignment.objects.filter(dorm=current_enrollment.dorm)
#                 if current_enrollment
#                 else []
#             )
#             context.update({
#                 'role': 'Resident',
#                 'user_data': resident,
#                 'current_enrollment': current_enrollment,
#                 'staff_assignments': staff_assignments,
#             })

#         elif hasattr(user_cred, 'staffs'):
#             # Fetch Staff-specific data
#             staff = user_cred.staffs  # Related object from OneToOneField
#             current_assignment = (
#                 StaffAssignment.objects.filter(staff=staff)
#                 .order_by('-created_at')
#                 .first()
#             )
#             context.update({
#                 'role': 'Staff',
#                 'user_data': staff,
#                 'current_assignment': current_assignment,
#             })

#         else:
#             # If user is neither a Resident nor a Staff
#             context['error'] = "No profile data found for this user."

#     except UserCred.DoesNotExist:
#         context['error'] = "UserCred profile not found."
#     except Exception as e:
#         # Catch unexpected errors for debugging
#         context['error'] = f"An error occurred: {str(e)}"

#     # Pass the updated context to the default admin index view
#     extra_context = extra_context or {}
#     extra_context.update(context)

#     return site.index(request, extra_context=extra_context)

# from django.contrib.admin.sites import site
# from django.shortcuts import render
# from UserProfiles.models import UserCred, Residents, Staffs
# from AcademicYear.models import Enrollment, StaffAssignment
# import logging

# # Setting up logger for error logging
# logger = logging.getLogger(__name__)

# def custom_admin_index(request, extra_context=None):
#     """
#     Custom admin index page to display user-specific data without disrupting the default admin.
#     """
#     user = request.user
#     context = {'role': None}  # Default context with no role

#     # Debugging: Ensure the user is authenticated
#     if not user.is_authenticated:
#         context['error'] = "User is not logged in."
#         return site.index(request, extra_context=extra_context)

#     try:
#         # Access the UserCred instance
#         user_cred = UserCred.objects.get(email=user.email)

#         if user_cred.is_resident:
#             # Fetch Resident-specific data
#             resident = user_cred.residents  # Accessing the related Resident object via OneToOneField
#             current_enrollment = (
#                 Enrollment.objects.filter(resident=resident, status='active')
#                 .order_by('-date_enrolled')
#                 .first()
#             )
#             staff_assignments = (
#                 StaffAssignment.objects.filter(dorm=current_enrollment.dorm)
#                 if current_enrollment
#                 else []
#             )
#             context.update({
#                 'role': 'Resident',
#                 'user_data': resident,
#                 'current_enrollment': current_enrollment,
#                 'staff_assignments': staff_assignments,
#             })

#         elif hasattr(user_cred, 'staffs'):
#             # Fetch Staff-specific data
#             staff = user_cred.staffs  # Related object from OneToOneField
#             current_assignment = (
#                 StaffAssignment.objects.filter(staff=staff)
#                 .order_by('-created_at')
#                 .first()
#             )
#             context.update({
#                 'role': 'Staff',
#                 'user_data': staff,
#                 'current_assignment': current_assignment,
#             })

#         else:
#             # If user is neither a Resident nor a Staff
#             context['error'] = "No profile data found for this user."

#     except UserCred.DoesNotExist:
#         context['error'] = "UserCred profile not found."
#         logger.error(f"UserCred not found for email: {user.email}")
#     except Exception as e:
#         # Catch unexpected errors for debugging
#         context['error'] = f"An error occurred: {str(e)}"
#         logger.error(f"Error in custom_admin_index: {str(e)}")

#     # Pass the updated context to the default admin index view
#     extra_context = extra_context or {}
#     extra_context.update(context)

#     return site.index(request, extra_context=extra_context)
