from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import AcademicSession, Semester, Enrollment, StaffAssignment


def index(request):
    return HttpResponse("Welcome to Dorms Section.")


# ACADEMIC SESSION
class AcademicSessionListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = AcademicSession
    template_name = 'academic_year/academic_session_list.html'
    context_object_name = 'sessions'
    login_url = 'login'
    permission_required = 'admin.view_academic_session'

class AcademicSessionDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = AcademicSession
    template_name = 'academic_year/academic_session_detail.html'
    context_object_name = 'session'
    login_url = 'login'
    permission_required = 'admin.view_academic_session'

class AcademicSessionCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = AcademicSession
    fields = ['start_year', 'end_year']
    template_name = 'academic_year/academic_session_form.html'
    success_url = reverse_lazy('academic_session_list')
    login_url = 'login'
    permission_required = 'admin.add_academic_session'

class AcademicSessionUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = AcademicSession
    fields = ['start_year', 'end_year']
    template_name = 'academic_year/academic_session_form.html'
    success_url = reverse_lazy('academic_session_list')
    login_url = 'login'
    permission_required = 'admin.change_academic_session'

class AcademicSessionDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = AcademicSession
    template_name = 'academic_year/academic_session_confirm_delete.html'
    success_url = reverse_lazy('academic_session_list')
    login_url = 'login'
    permission_required = 'admin.delete_academic_session'

# SEMESTER
class SemesterListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Semester
    template_name = 'academic_year/semester_list.html'
    context_object_name = 'semesters'
    login_url = 'login'
    permission_required = 'admin.view_semester'

class SemesterDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Semester
    template_name = 'academic_year/semester_detail.html'
    context_object_name = 'semester'
    login_url = 'login'
    permission_required = 'admin.view_semester'

class SemesterCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Semester
    fields = ['semester_type', 'start_date', 'end_date', 'academic_session']
    template_name = 'academic_year/semester_form.html'
    success_url = reverse_lazy('semester_list')
    login_url = 'login'
    permission_required = 'admin.add_semester'

class SemesterUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Semester
    fields = ['semester_type', 'start_date', 'end_date', 'academic_session']
    template_name = 'academic_year/semester_form.html'
    success_url = reverse_lazy('semester_list')
    login_url = 'login'
    permission_required = 'admin.change_semester'

class SemesterDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Semester
    template_name = 'academic_year/semester_confirm_delete.html'
    success_url = reverse_lazy('semester_list')
    login_url = 'login'
    permission_required = 'admin.delete_semester'

# ENROLLMENT
class EnrollmentListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Enrollment
    template_name = 'academic_year/enrollment_list.html'
    context_object_name = 'enrollments'
    login_url = 'login'
    permission_required = 'admin.view_enrollment'

class EnrollmentDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Enrollment
    template_name = 'academic_year/enrollment_detail.html'
    context_object_name = 'enrollment'
    login_url = 'login'
    permission_required = 'admin.view_enrollment'

class EnrollmentCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Enrollment
    fields = ['resident', 'semester', 'academic_session', 'dorm', 'room']
    template_name = 'academic_year/enrollment_form.html'
    success_url = reverse_lazy('enrollment_list')
    login_url = 'login'
    permission_required = 'admin.add_enrollment'

class EnrollmentUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Enrollment
    fields = ['resident', 'semester', 'academic_session', 'dorm', 'room']
    template_name = 'academic_year/enrollment_form.html'
    success_url = reverse_lazy('enrollment_list')
    login_url = 'login'
    permission_required = 'admin.change_enrollment'

class EnrollmentDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Enrollment
    template_name = 'academic_year/enrollment_confirm_delete.html'
    success_url = reverse_lazy('enrollment_list')
    login_url = 'login'
    permission_required = 'admin.delete_enrollment'

# STAFF ASSIGNMENT
class StaffAssignmentListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = StaffAssignment
    template_name = 'academic_year/staff_assignment_list.html'
    context_object_name = 'assignments'
    login_url = 'login'
    permission_required = 'admin.view_staffassignment'

class StaffAssignmentDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = StaffAssignment
    template_name = 'academic_year/staff_assignment_detail.html'
    context_object_name = 'assignment'
    login_url = 'login'
    permission_required = 'admin.view_staffassignment'

class StaffAssignmentCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = StaffAssignment
    fields = ['staff', 'dorm', 'role', 'academic_session', 'semester']
    template_name = 'academic_year/staff_assignment_form.html'
    success_url = reverse_lazy('staff_assignment_list')
    login_url = 'login'
    permission_required = 'admin.add_staffassignment'

class StaffAssignmentUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = StaffAssignment
    fields = ['staff', 'dorm', 'role', 'academic_session', 'semester']
    template_name = 'academic_year/staff_assignment_form.html'
    success_url = reverse_lazy('staff_assignment_list')
    login_url = 'login'
    permission_required = 'admin.change_staffassignment'

class StaffAssignmentDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = StaffAssignment
    template_name = 'academic_year/staff_assignment_confirm_delete.html'
    success_url = reverse_lazy('staff_assignment_list')
    login_url = 'login'
    permission_required = 'admin.delete_staffassignment'



class LogoutView(LogoutView):
    next_page = reverse_lazy('login')