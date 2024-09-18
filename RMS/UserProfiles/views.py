from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import UserCred, Residents, Roles, Staffs
from .forms import StaffRegistrationForm, StaffLoginForm, ResidentRegistrationForm, ResidentLoginForm, EmailAuthenticationForm
from django.conf import settings

# '''USERCRED'''
# class UserCredListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
#     model = UserCred
#     template_name = 'userprofiles/usercred_list.html'
#     context_object_name = 'users'
#     login_url = 'login'
#     permission_required = 'userprofiles.view_usercred'

# class UserCredDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
#     model = UserCred
#     template_name = 'userprofiles/usercred_detail.html'
#     context_object_name = 'user'
#     login_url = 'login'
#     permission_required = 'userprofiles.view_usercred'

# class UserCredCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
#     model = UserCred
#     form_class = StaffRegistrationForm
#     template_name = 'userprofiles/usercred_form.html'
#     success_url = reverse_lazy('usercred_list')
#     login_url = 'login'
#     permission_required = 'userprofiles.add_usercred'

# class UserCredUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
#     model = UserCred
#     form_class = StaffRegistrationForm
#     template_name = 'userprofiles/usercred_form.html'
#     success_url = reverse_lazy('usercred_list')
#     login_url = 'login'
#     permission_required = 'userprofiles.change_usercred'

# class UserCredDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
#     model = UserCred
#     template_name = 'userprofiles/usercred_confirm_delete.html'
#     success_url = reverse_lazy('usercred_list')
#     login_url = 'login'
#     permission_required = 'userprofiles.delete_usercred'


# '''RESIDENT'''
# class ResidentRegistrationView(CreateView):
#     form_class = ResidentRegistrationForm
#     template_name = 'accounts/registration/resident_registration.html'
#     success_url = reverse_lazy('resident_login')

# class ResidentLoginView(LoginView):
#     template_name = 'userprofiles/resident_login.html'
#     form_class = ResidentLoginForm
#     success_url = reverse_lazy('resident_dashboard')

#     def form_valid(self, form):
#         email = form.cleaned_data['email']
#         room_number = form.cleaned_data['room_number']
#         password = form.cleaned_data['password']
#         user = authenticate(self.request, email=email, room_number=room_number, password=password)
#         if user is not None and not user.is_staff:
#             login(self.request, user)
#             return redirect(self.success_url)
#         else:
#             return self.form_invalid(form)

# class ResidentDashboardView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
#     model = Residents
#     template_name = 'userprofiles/resident_dashboard.html'
#     context_object_name = 'residents'
#     login_url = 'login'
#     permission_required = 'userprofiles.view_residents'

# class ResidentsListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
#     model = Residents
#     template_name = 'userprofiles/residents_list.html'
#     context_object_name = 'residents'
#     login_url = 'login'
#     permission_required = 'userprofiles.view_residents'

# class ResidentsDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
#     model = Residents
#     template_name = 'userprofiles/residents_detail.html'
#     context_object_name = 'resident'
#     login_url = 'login'
#     permission_required = 'userprofiles.view_residents'

# class ResidentsCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
#     model = Residents
#     fields = ['user', 'guardian_phone_number']
#     template_name = 'userprofiles/residents_form.html'
#     success_url = reverse_lazy('residents_list')
#     login_url = 'login'
#     permission_required = 'userprofiles.add_residents'

# class ResidentsUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
#     model = Residents
#     fields = ['guardian_phone_number']
#     template_name = 'userprofiles/residents_form.html'
#     success_url = reverse_lazy('residents_list')
#     login_url = 'login'
#     permission_required = 'userprofiles.change_residents'

# class ResidentsDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
#     model = Residents
#     template_name = 'userprofiles/residents_confirm_delete.html'
#     success_url = reverse_lazy('residents_list')
#     login_url = 'login'
#     permission_required = 'userprofiles.delete_residents'


# '''STAFF'''

# class StaffRegistrationView(CreateView):
#     form_class = StaffRegistrationForm
#     template_name = 'userprofiles/staff_registration.html'
#     success_url = reverse_lazy('staff_login')

# class StaffLoginView(LoginView):
#     template_name = 'userprofiles/staff_login.html'
#     form_class = StaffLoginForm
#     success_url = reverse_lazy('staff_dashboard')

#     def form_valid(self, form):
#         email = form.cleaned_data['email']
#         password = form.cleaned_data['password']
#         user = authenticate(self.request, email=email, password=password)
#         if user is not None and user.is_staff:
#             login(self.request, user)
#             return redirect(self.success_url)
#         else:
#             return self.form_invalid(form)

# class StaffDashboardView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
#     model = Staffs
#     template_name = 'userprofiles/staff_dashboard.html'
#     context_object_name = 'staffs'
#     login_url = 'login'
#     permission_required = 'userprofiles.view_staffs'

# class StaffsListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
#     model = Staffs
#     template_name = 'userprofiles/staffs_list.html'
#     context_object_name = 'staffs'
#     login_url = 'login'
#     permission_required = 'userprofiles.view_staffs'

# class StaffsDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
#     model = Staffs
#     template_name = 'userprofiles/staffs_detail.html'
#     context_object_name = 'staff'
#     login_url = 'login'
#     permission_required = 'userprofiles.view_staffs'

# class StaffsCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
#     model = Staffs
#     fields = ['user', 'role']
#     template_name = 'userprofiles/staffs_form.html'
#     success_url = reverse_lazy('staffs_list')
#     login_url = 'login'
#     permission_required = 'userprofiles.add_staffs'

# class StaffsUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
#     model = Staffs
#     fields = ['role']
#     template_name = 'userprofiles/staffs_form.html'
#     success_url = reverse_lazy('staffs_list')
#     login_url = 'login'
#     permission_required = 'userprofiles.change_staffs'

# class StaffsDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
#     model = Staffs
#     template_name = 'userprofiles/staffs_confirm_delete.html'
#     success_url = reverse_lazy('staffs_list')
#     login_url = 'login'
#     permission_required = 'userprofiles.delete_staffs'


# '''ROLES'''
# class RolesListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
#     model = Roles
#     template_name = 'userprofiles/roles_list.html'
#     context_object_name = 'roles'
#     login_url = 'login'
#     permission_required = 'userprofiles.view_roles'

# class RolesDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
#     model = Roles
#     template_name = 'userprofiles/roles_detail.html'
#     context_object_name = 'role'
#     login_url = 'login'
#     permission_required = 'userprofiles.view_roles'

# class RolesCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
#     model = Roles
#     fields = ['name', 'abbreviation']
#     template_name = 'userprofiles/roles_form.html'
#     success_url = reverse_lazy('roles_list')
#     login_url = 'login'
#     permission_required = 'userprofiles.add_roles'

# class RolesUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
#     model = Roles
#     fields = ['name', 'abbreviation']
#     template_name = 'userprofiles/roles_form.html'
#     success_url = reverse_lazy('roles_list')
#     login_url = 'login'
#     permission_required = 'userprofiles.change_roles'

# class RolesDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
#     model = Roles
#     template_name = 'userprofiles/roles_confirm_delete.html'
#     success_url = reverse_lazy('roles_list')
#     login_url = 'login'
#     permission_required = 'userprofiles.delete_roles'

# # Logout View
# class LogoutView(LogoutView):
#     next_page = reverse_lazy('login')

def index(request):
    return HttpResponse("Welcome to AUN ResLife App.")


# '''DJANGO ADMIN'''
# class CustomAdminLoginView(LoginView):
#     template_name = 'registration/admin_login.html'
#     authentication_form = EmailAuthenticationForm

#     def form_valid(self, form):
#         email = form.cleaned_data.get('username')
#         password = form.cleaned_data.get('password')
#         user = authenticate(request=self.request, email=email, password=password)
#         if user is not None:
#             login(self.request, user)
#             return redirect('admin:index')
#         else:
#             form.add_error(None, 'Invalid email or password.')
#             return self.form_invalid(form)