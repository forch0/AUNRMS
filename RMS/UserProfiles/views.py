from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import UserCred, Residents, Roles, Staffs
from .forms import StaffRegistrationForm, StaffLoginForm, ResidentRegistrationForm, ResidentLoginForm

'''USERCRED'''
class UserCredListView(LoginRequiredMixin, ListView):
    model = UserCred
    template_name = 'userprofiles/usercred_list.html'
    context_object_name = 'users'
    login_url = 'login'

class UserCredDetailView(LoginRequiredMixin, DetailView):
    model = UserCred
    template_name = 'userprofiles/usercred_detail.html'
    context_object_name = 'user'
    login_url = 'login'

class UserCredCreateView(LoginRequiredMixin, CreateView):
    model = UserCred
    form_class = StaffRegistrationForm
    template_name = 'userprofiles/usercred_form.html'
    success_url = reverse_lazy('usercred_list')
    login_url = 'login'

class UserCredUpdateView(LoginRequiredMixin, UpdateView):
    model = UserCred
    form_class = StaffRegistrationForm
    template_name = 'userprofiles/usercred_form.html'
    success_url = reverse_lazy('usercred_list')
    login_url = 'login'

class UserCredDeleteView(LoginRequiredMixin, DeleteView):
    model = UserCred
    template_name = 'userprofiles/usercred_confirm_delete.html'
    success_url = reverse_lazy('usercred_list')
    login_url = 'login'


'''RESIDENT'''
class ResidentRegistrationView(CreateView):
    form_class = ResidentRegistrationForm
    template_name = 'userprofiles/resident_registration.html'
    success_url = reverse_lazy('resident_login')

class ResidentLoginView(LoginView):
    template_name = 'userprofiles/resident_login.html'
    form_class = ResidentLoginForm
    success_url = reverse_lazy('resident_dashboard')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        room_number = form.cleaned_data['room_number']
        password = form.cleaned_data['password']
        user = authenticate(self.request, email=email, room_number=room_number, password=password)
        if user is not None and not user.is_staff:
            login(self.request, user)
            return redirect(self.success_url)
        else:
            return self.form_invalid(form)

class ResidentDashboardView(LoginRequiredMixin, ListView):
    model = Residents
    template_name = 'userprofiles/resident_dashboard.html'
    context_object_name = 'residents'
    login_url = 'login'

class ResidentsListView(LoginRequiredMixin, ListView):
    model = Residents
    template_name = 'userprofiles/residents_list.html'
    context_object_name = 'residents'
    login_url = 'login'

class ResidentsDetailView(LoginRequiredMixin, DetailView):
    model = Residents
    template_name = 'userprofiles/residents_detail.html'
    context_object_name = 'resident'
    login_url = 'login'

class ResidentsCreateView(LoginRequiredMixin, CreateView):
    model = Residents
    fields = ['user', 'guardian_phone_number']
    template_name = 'userprofiles/residents_form.html'
    success_url = reverse_lazy('residents_list')
    login_url = 'login'

class ResidentsUpdateView(LoginRequiredMixin, UpdateView):
    model = Residents
    fields = ['guardian_phone_number']
    template_name = 'userprofiles/residents_form.html'
    success_url = reverse_lazy('residents_list')
    login_url = 'login'

class ResidentsDeleteView(LoginRequiredMixin, DeleteView):
    model = Residents
    template_name = 'userprofiles/residents_confirm_delete.html'
    success_url = reverse_lazy('residents_list')
    login_url = 'login'



'''STAFF'''

class StaffRegistrationView(CreateView):
    form_class = StaffRegistrationForm
    template_name = 'userprofiles/staff_registration.html'
    success_url = reverse_lazy('staff_login')

class StaffLoginView(LoginView):
    template_name = 'userprofiles/staff_login.html'
    form_class = StaffLoginForm
    success_url = reverse_lazy('staff_dashboard')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(self.request, email=email, password=password)
        if user is not None and user.is_staff:
            login(self.request, user)
            return redirect(self.success_url)
        else:
            return self.form_invalid(form)

class StaffDashboardView(LoginRequiredMixin, ListView):
    model = Staffs
    template_name = 'userprofiles/staff_dashboard.html'
    context_object_name = 'staffs'
    login_url = 'login'

class StaffsListView(LoginRequiredMixin, ListView):
    model = Staffs
    template_name = 'userprofiles/staffs_list.html'
    context_object_name = 'staffs'
    login_url = 'login'
class StaffsDetailView(LoginRequiredMixin, DetailView):
    model = Staffs
    template_name = 'userprofiles/staffs_detail.html'
    context_object_name = 'staff'
    login_url = 'login'

class StaffsCreateView(LoginRequiredMixin, CreateView):
    model = Staffs
    fields = ['user', 'role']
    template_name = 'userprofiles/staffs_form.html'
    success_url = reverse_lazy('staffs_list')
    login_url = 'login'

class StaffsUpdateView(LoginRequiredMixin, UpdateView):
    model = Staffs
    fields = ['role']
    template_name = 'userprofiles/staffs_form.html'
    success_url = reverse_lazy('staffs_list')
    login_url = 'login'

class StaffsDeleteView(LoginRequiredMixin, DeleteView):
    model = Staffs
    template_name = 'userprofiles/staffs_confirm_delete.html'
    success_url = reverse_lazy('staffs_list')
    login_url = 'login'


'''ROLES'''
class RolesListView(LoginRequiredMixin, ListView):
    model = Roles
    template_name = 'userprofiles/roles_list.html'
    context_object_name = 'roles'
    login_url = 'login'

class RolesDetailView(LoginRequiredMixin, DetailView):
    model = Roles
    template_name = 'userprofiles/roles_detail.html'
    context_object_name = 'role'
    login_url = 'login'

class RolesCreateView(LoginRequiredMixin, CreateView):
    model = Roles
    fields = ['name', 'abbreviation']
    template_name = 'userprofiles/roles_form.html'
    success_url = reverse_lazy('roles_list')
    login_url = 'login'

class RolesUpdateView(LoginRequiredMixin, UpdateView):
    model = Roles
    fields = ['name', 'abbreviation']
    template_name = 'userprofiles/roles_form.html'
    success_url = reverse_lazy('roles_list')
    login_url = 'login'

class RolesDeleteView(LoginRequiredMixin, DeleteView):
    model = Roles
    template_name = 'userprofiles/roles_confirm_delete.html'
    success_url = reverse_lazy('roles_list')
    login_url = 'login'


# Logout View
class LogoutView(LogoutView):
    next_page = reverse_lazy('login')

def index(request):
    return HttpResponse("Welcome to AUN ResLife App.")
