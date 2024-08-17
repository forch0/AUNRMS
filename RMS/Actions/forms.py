from django import forms
from .models import Category, SubCategory, MaintenanceRequest, Announcement, Complaint

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = ['name', 'category']

class MaintenanceRequestForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRequest
        fields = [
            'dorm', 'room', 'resident', 'semester', 'academic_session',
            'category', 'sub_category', 'description', 'status', 'updated_by'
        ]

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = [
            'title', 'message', 'created_by', 'dorms', 'is_global',
            'semester', 'academic_session'
        ]

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['user', 'enrollment', 'semester', 'academic_session', 'description', 'is_anonymous']
