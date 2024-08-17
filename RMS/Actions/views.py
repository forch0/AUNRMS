# Import necessary modules and forms
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import *
from .forms import *
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

def index(request):
    return HttpResponse("Welcome to Operations Section.")

# Maintenance Request Views

class MaintenanceRequestListView(LoginRequiredMixin, ListView):
    model = MaintenanceRequest
    template_name = 'actions/maintenance_request_list.html'
    context_object_name = 'maintenance_requests'

    def get_queryset(self):
        # Filter based on user permissions or specific criteria
        return MaintenanceRequest.objects.all()

class MaintenanceRequestDetailView(LoginRequiredMixin, DetailView):
    model = MaintenanceRequest
    template_name = 'actions/maintenance_request_detail.html'
    context_object_name = 'maintenance_request'

class MaintenanceRequestCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = MaintenanceRequest
    form_class = MaintenanceRequestForm
    template_name = 'actions/maintenance_request_form.html'
    permission_required = 'actions.add_maintenancerequest'

    def form_valid(self, form):
        form.instance.resident = self.request.user  # Automatically set the current user as the resident
        return super().form_valid(form)

class MaintenanceRequestUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = MaintenanceRequest
    form_class = MaintenanceRequestForm
    template_name = 'actions/maintenance_request_form.html'
    permission_required = 'actions.change_maintenancerequest'

    def form_valid(self, form):
        form.instance.updated_by = self.request.user  # Automatically set the current user as the updater
        return super().form_valid(form)

class MaintenanceRequestDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = MaintenanceRequest
    template_name = 'actions/maintenance_request_confirm_delete.html'
    success_url = reverse_lazy('maintenance_request_list')
    permission_required = 'actions.delete_maintenancerequest'

# Announcement Views

class AnnouncementListView(LoginRequiredMixin, ListView):
    model = Announcement
    template_name = 'actions/announcement_list.html'
    context_object_name = 'announcements'

    def get_queryset(self):
        user = self.request.user
        if user.role.name == 'ResLife Director':
            return Announcement.objects.all()
        return Announcement.objects.filter(dorms__in=user.dorms.all())

class AnnouncementDetailView(LoginRequiredMixin, DetailView):
    model = Announcement
    template_name = 'actions/announcement_detail.html'
    context_object_name = 'announcement'

class AnnouncementCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Announcement
    form_class = AnnouncementForm
    template_name = 'actions/announcement_form.html'
    permission_required = 'actions.add_announcement'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class AnnouncementUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Announcement
    form_class = AnnouncementForm
    template_name = 'actions/announcement_form.html'
    permission_required = 'actions.change_announcement'

class AnnouncementDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Announcement
    template_name = 'actions/announcement_confirm_delete.html'
    success_url = reverse_lazy('announcement_list')
    permission_required = 'actions.delete_announcement'

# Complaint Views

class ComplaintListView(LoginRequiredMixin, ListView):
    model = Complaint
    template_name = 'actions/complaint_list.html'
    context_object_name = 'complaints'

    def get_queryset(self):
        return Complaint.objects.all()

class ComplaintDetailView(LoginRequiredMixin, DetailView):
    model = Complaint
    template_name = 'actions/complaint_detail.html'
    context_object_name = 'complaint'

class ComplaintCreateView(LoginRequiredMixin, CreateView):
    model = Complaint
    form_class = ComplaintForm
    template_name = 'actions/complaint_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ComplaintUpdateView(LoginRequiredMixin, UpdateView):
    model = Complaint
    form_class = ComplaintForm
    template_name = 'actions/complaint_form.html'

class ComplaintDeleteView(LoginRequiredMixin, DeleteView):
    model = Complaint
    template_name = 'actions/complaint_confirm_delete.html'
    success_url = reverse_lazy('complaint_list')


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'actions/category_list.html'
    context_object_name = 'categories'

class CategoryDetailView(LoginRequiredMixin, DetailView):
    model = Category
    template_name = 'actions/category_detail.html'
    context_object_name = 'category'

class CategoryCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'actions/category_form.html'
    permission_required = 'actions.add_category'

class CategoryUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'actions/category_form.html'
    permission_required = 'actions.change_category'

class CategoryDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Category
    template_name = 'actions/category_confirm_delete.html'
    success_url = reverse_lazy('category_list')
    permission_required = 'actions.delete_category'

# SubCategory Views

class SubCategoryListView(LoginRequiredMixin, ListView):
    model = SubCategory
    template_name = 'actions/subcategory_list.html'
    context_object_name = 'subcategories'

class SubCategoryDetailView(LoginRequiredMixin, DetailView):
    model = SubCategory
    template_name = 'actions/subcategory_detail.html'
    context_object_name = 'subcategory'

class SubCategoryCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = SubCategory
    form_class = SubCategoryForm
    template_name = 'actions/subcategory_form.html'
    permission_required = 'actions.add_subcategory'

class SubCategoryUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = SubCategory
    form_class = SubCategoryForm
    template_name = 'actions/subcategory_form.html'
    permission_required = 'actions.change_subcategory'

class SubCategoryDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = SubCategory
    template_name = 'actions/subcategory_confirm_delete.html'
    success_url = reverse_lazy('subcategory_list')
    permission_required = 'actions.delete_subcategory'