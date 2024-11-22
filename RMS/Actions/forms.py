from django import forms
from .models import Category, SubCategory, MaintenanceRequest, Announcement, Complaint
from AcademicYear.models import * 
from Dorms.models import * 
from django.core.exceptions import ValidationError

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


# class AnnouncementForm(forms.ModelForm):
#     class Meta:
#         model = Announcement
#         fields = '__all__'

#     def clean(self):
#         cleaned_data = super().clean()
#         is_global = cleaned_data.get('is_global')
#         dorms = cleaned_data.get('dorms')
#         created_by = cleaned_data.get('created_by')

#         # Ensure the created_by user exists
#         if not created_by:
#             raise ValidationError("The 'created by' field is required.")

#         # Ensure the user has a Staffs profile
#         staff_profile = getattr(created_by, 'staffs', None)
#         if not staff_profile:
#             raise ValidationError("The selected user is not a staff member.")

#         # Validate global announcement permissions
#         if is_global and not staff_profile.role.name == 'ResLife Director':
#             raise ValidationError("Only ResLife Directors can create global announcements.")

#         # Validate dorms for non-global announcements
#         if not is_global:
#             if not dorms or dorms.count() == 0:
#                 raise ValidationError("You must specify at least one dorm for non-global announcements.")

#             # Ensure staff is assigned to the selected dorms
#             assigned_dorms = Dorm.objects.filter(staffassignment__staff=staff_profile).values_list('id', flat=True)
#             for dorm in dorms:
#                 if dorm.id not in assigned_dorms:
#                     raise ValidationError(f"You are not assigned to the dorm: {dorm.name}.")

#         return cleaned_data

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        is_global = cleaned_data.get('is_global')
        dorms = cleaned_data.get('dorms')
        created_by = cleaned_data.get('created_by')

        # Ensure the created_by user exists
        if not created_by:
            raise ValidationError("The 'created by' field is required.")

        # Ensure the 'created_by' is a valid Staffs instance, not UserCred
        staff_profile = getattr(created_by, 'staffs', None)
        if not staff_profile:
            raise ValidationError(f"The selected user {created_by.email} is not a staff member.")

        # Validate global announcement permissions
        if is_global and not staff_profile.role.name == 'ResLife Director':
            raise ValidationError("Only ResLife Directors can create global announcements.")

        # Validate dorms for non-global announcements
        if not is_global:
            if not dorms or dorms.count() == 0:
                raise ValidationError("You must specify at least one dorm for non-global announcements.")

            # Ensure staff is assigned to the selected dorms
            assigned_dorms = Dorm.objects.filter(staffassignment__staff=staff_profile).values_list('id', flat=True)
            for dorm in dorms:
                if dorm.id not in assigned_dorms:
                    raise ValidationError(f"You are not assigned to the dorm: {dorm.name}.")

        # Set the 'created_by' field to the corresponding Staffs instance, if it's not set
        if created_by:
            staff_instance = getattr(created_by, 'staffs', None)
            if staff_instance:
                cleaned_data['created_by'] = staff_instance  # Set the correct Staffs instance

        return cleaned_data


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