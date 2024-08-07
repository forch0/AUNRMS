# Import necessary modules and forms
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
# from .models import Category, SubCategory, MaintenanceRequest, Announcement, Complaint
# from .forms import CategoryForm, SubCategoryForm, MaintenanceRequestForm, AnnouncementForm, ComplaintForm
from django.http import HttpResponse

def index(request):
    return HttpResponse("Welcome to Operations Section.")
# Category Views
# class CategoryListView(ListView):
#     model = Category
#     template_name = 'category_list.html'

# class CategoryDetailView(DetailView):
#     model = Category
#     template_name = 'category_detail.html'

# class CategoryCreateView(CreateView):
#     model = Category
#     form_class = CategoryForm
#     template_name = 'category_form.html'
#     success_url = reverse_lazy('category_list')

# class CategoryUpdateView(UpdateView):
#     model = Category
#     form_class = CategoryForm
#     template_name = 'category_form.html'
#     success_url = reverse_lazy('category_list')

# class CategoryDeleteView(DeleteView):
#     model = Category
#     template_name = 'category_confirm_delete.html'
#     success_url = reverse_lazy('category_list')

# # SubCategory Views
# class SubCategoryListView(ListView):
#     model = SubCategory
#     template_name = 'subcategory_list.html'

# class SubCategoryDetailView(DetailView):
#     model = SubCategory
#     template_name = 'subcategory_detail.html'

# class SubCategoryCreateView(CreateView):
#     model = SubCategory
#     form_class = SubCategoryForm
#     template_name = 'subcategory_form.html'
#     success_url = reverse_lazy('subcategory_list')

# class SubCategoryUpdateView(UpdateView):
#     model = SubCategory
#     form_class = SubCategoryForm
#     template_name = 'subcategory_form.html'
#     success_url = reverse_lazy('subcategory_list')

# class SubCategoryDeleteView(DeleteView):
#     model = SubCategory
#     template_name = 'subcategory_confirm_delete.html'
#     success_url = reverse_lazy('subcategory_list')

# # MaintenanceRequest Views
# class MaintenanceRequestListView(ListView):
#     model = MaintenanceRequest
#     template_name = 'maintenancerequest_list.html'

# class MaintenanceRequestDetailView(DetailView):
#     model = MaintenanceRequest
#     template_name = 'maintenancerequest_detail.html'

# class MaintenanceRequestCreateView(CreateView):
#     model = MaintenanceRequest
#     form_class = MaintenanceRequestForm
#     template_name = 'maintenancerequest_form.html'
#     success_url = reverse_lazy('maintenancerequest_list')

# class MaintenanceRequestUpdateView(UpdateView):
#     model = MaintenanceRequest
#     form_class = MaintenanceRequestForm
#     template_name = 'maintenancerequest_form.html'
#     success_url = reverse_lazy('maintenancerequest_list')

# class MaintenanceRequestDeleteView(DeleteView):
#     model = MaintenanceRequest
#     template_name = 'maintenancerequest_confirm_delete.html'
#     success_url = reverse_lazy('maintenancerequest_list')

# # Announcement Views
# class AnnouncementListView(ListView):
#     model = Announcement
#     template_name = 'announcement_list.html'

# class AnnouncementDetailView(DetailView):
#     model = Announcement
#     template_name = 'announcement_detail.html'

# class AnnouncementCreateView(CreateView):
#     model = Announcement
#     form_class = AnnouncementForm
#     template_name = 'announcement_form.html'
#     success_url = reverse_lazy('announcement_list')

# class AnnouncementUpdateView(UpdateView):
#     model = Announcement
#     form_class = AnnouncementForm
#     template_name = 'announcement_form.html'
#     success_url = reverse_lazy('announcement_list')

# class AnnouncementDeleteView(DeleteView):
#     model = Announcement
#     template_name = 'announcement_confirm_delete.html'
#     success_url = reverse_lazy('announcement_list')

# # Complaint Views
# class ComplaintListView(ListView):
#     model = Complaint
#     template_name = 'complaint_list.html'

# class ComplaintDetailView(DetailView):
#     model = Complaint
#     template_name = 'complaint_detail.html'

# class ComplaintCreateView(CreateView):
#     model = Complaint
#     form_class = ComplaintForm
#     template_name = 'complaint_form.html'
#     success_url = reverse_lazy('complaint_list')

# class ComplaintUpdateView(UpdateView):
#     model = Complaint
#     form_class = ComplaintForm
#     template_name = 'complaint_form.html'
#     success_url = reverse_lazy('complaint_list')

# class ComplaintDeleteView(DeleteView):
#     model = Complaint
#     template_name = 'complaint_confirm_delete.html'
#     success_url = reverse_lazy('complaint_list')


