from django import forms
from .models import Category, SubCategory, MaintenanceRequest, Announcement, Complaint
from AcademicYear.models import Enrollment
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
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        user = cleaned_data.get('user')
        enrollment = cleaned_data.get('enrollment')
        semester = cleaned_data.get('semester')

        # Validation: User must be enrolled in the dorm for the given semester
        if user and enrollment and semester:
            if not Enrollment.objects.filter(
                user=user, 
                dorm=enrollment.dorm, 
                semester=semester
            ).exists():
                raise forms.ValidationError(
                    "You can only submit complaints for the dorm you are enrolled in during this semester."
                )

        return cleaned_data