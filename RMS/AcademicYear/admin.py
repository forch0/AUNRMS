from django.contrib import admin
from django.http import HttpRequest
from .models import AcademicSession, Semester, Enrollment, StaffAssignment
from .forms import SemesterForm
from Dorms.models import Dorm
from UserProfiles.models import Staffs, Roles, UserCred
from admin_confirm import AdminConfirmMixin
from typing import Any

@admin.register(AdminConfirmMixin,AcademicSession)
class AcademicSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'start_year', 'end_year')
    search_fields = ('name', 'start_year', 'end_year')
    ordering = ('start_year',)
    confirm_change= True
    confirmation_fields = ['start_year', 'end_year']

    def _is_superuser(self, request: HttpRequest) -> bool:
        """Checks if the user is a Django superuser."""
        return request.user.is_superuser
    
    def _has_selected_roles(self, request: HttpRequest) -> bool:
        """Checks if the user has one of the allowed roles."""
        allowed_roles = ['ResLife Directors',]  # Add the role names you want here
        staff = Staffs.objects.filter(user=request.user).first()
        if staff:
            return staff.role.name in allowed_roles
        return False
    
    def has_view_permission(self, request: HttpRequest, obj: Any | None = None) -> bool:
        """Allows selected roles and superuser to view the model."""
        return self._is_superuser(request) or self._has_selected_roles(request)

    def has_add_permission(self, request: HttpRequest) -> bool:
        """Only superuser can add."""
        return self._is_superuser(request)

    def has_change_permission(self, request: HttpRequest, obj: Any | None = None) -> bool:
        """Only superuser can change."""
        return self._is_superuser(request)

    def has_delete_permission(self, request: HttpRequest, obj: Any | None = None) -> bool:
        """Only superuser can delete."""
        return self._is_superuser(request)

# Registering the Semester model
@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    form = SemesterForm
    list_display = ('id', 'semester_type', 'start_date', 'end_date', 'academic_session')
    list_filter = ('semester_type', 'academic_session')
    fields = ('semester_type', 'start_date', 'end_date', 'academic_session')
    search_fields = ('semester_type', 'academic_session__name')
    ordering = ('start_date',)

    def _is_superuser(self, request: HttpRequest) -> bool:
        """Checks if the user is a Django superuser."""
        return request.user.is_superuser
    
    def _has_selected_roles(self, request: HttpRequest) -> bool:
        """Checks if the user has one of the allowed roles."""
        allowed_roles = ['ResLife Directors',]  # Add the role names you want here
        staff = Staffs.objects.filter(user=request.user).first()
        if staff:
            return staff.role.name in allowed_roles
        return False
    
    # def has_module_permission(self, request: HttpRequest) -> bool:
    #     return self._is_superuser(request) or self._has_selected_roles(request)
    
    def has_view_permission(self, request: HttpRequest, obj: Any | None = None) -> bool:
        """Allows selected roles and superuser to view the model."""
        return self._is_superuser(request) or self._has_selected_roles(request)

    def has_add_permission(self, request: HttpRequest) -> bool:
        """Only superuser can add."""
        return self._is_superuser(request)

    def has_change_permission(self, request: HttpRequest, obj: Any | None = None) -> bool:
        """Only superuser can change."""
        return self._is_superuser(request)

    def has_delete_permission(self, request: HttpRequest, obj: Any | None = None) -> bool:
        """Only superuser can delete."""
        return self._is_superuser(request)
    

    

    class Media:
        css = {
            'all': (
                'https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css',
                'https://cdnjs.cloudflare.com/ajax/libs/bootstrap-datepicker/1.9.0/css/bootstrap-datepicker.min.css',
            )
        }
        js = (
            'https://code.jquery.com/jquery-3.3.1.min.js',
            'https://cdnjs.cloudflare.com/ajax/libs/bootstrap-datepicker/1.9.0/js/bootstrap-datepicker.min.js',
            'js/datepicker_init.js',
        )

    # def get_form(self, request, obj=None, **kwargs):
    #     form = super().get_form(request, obj, **kwargs)
    #     form.base_fields['start_date'].widget.attrs.update({'class': 'datepicker'})
    #     form.base_fields['end_date'].widget.attrs.update({'class': 'datepicker'})
    #     return form

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        
        # Use .get() to avoid KeyError
        start_date_field = form.base_fields.get('start_date')
        end_date_field = form.base_fields.get('end_date')

        if start_date_field:
            start_date_field.widget.attrs.update({'class': 'datepicker'})
        if end_date_field:
            end_date_field.widget.attrs.update({'class': 'datepicker'})
        
        return form

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'resident', 'semester', 'academic_session', 'dorm', 'room', 'date_enrolled')
    list_filter = ('semester', 'academic_session', 'dorm', 'room')
    ordering = ('date_enrolled',)
    confirmation_fields = ['resident',]

    def _is_superuser(self, request: HttpRequest) -> bool:
        """Checks if the user is a Django superuser."""
        return request.user.is_superuser
    
    def _is_reslife_director(self, request: HttpRequest) -> bool:
        """Checks if the user is a ResLife Director."""
        staff = Staffs.objects.filter(user=request.user).first()
        return staff and staff.role.name == 'ResLife Director'

    def _is_residence_director(self, request: HttpRequest) -> bool:
        """Checks if the user is a Residence Director."""
        staff = Staffs.objects.filter(user=request.user).first()
        return staff and staff.role.name == 'Residence Director'
    
    def _is_residence_assistant(self, request: HttpRequest) -> bool:
        """Checks if the user is a Residence Assistant."""
        staff = Staffs.objects.filter(user=request.user).first()
        return staff and staff.role.name == 'Residence Assistant'
    
    def has_view_permission(self, request: HttpRequest, obj: Enrollment | None = None) -> bool:
        """Allows superusers, residents, and specific roles to view their enrollments."""
        if self._is_superuser(request):
            return True

        allowed_roles_all = ['ResLife Director', 'Dean of Student Affairs']
        if request.user.is_authenticated:
            staff = Staffs.objects.filter(user=request.user).first()
            if staff and staff.role.name in allowed_roles_all:
                return True

            if hasattr(request.user, 'resident'):
                return True  # Allow residents to view their enrollments

            if staff and staff.role.name in ['Residence Assistant', 'Residence Director']:
                return True  # Allow them to view, but filtering will occur in get_queryset

        return False  # No other roles can view enrollments
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if self._is_superuser(request):
            return qs  

        allowed_roles_all = ['ResLife Director', 'Dean of Student Affairs']
        if request.user.is_authenticated:
            staff = Staffs.objects.filter(user=request.user).first()
            if staff and staff.role.name in allowed_roles_all:
                return qs  # Return all enrollments for these roles

            if hasattr(request.user, 'resident'):
                return qs.filter(resident=request.user.resident)  # Filter for the resident's enrollments

            if staff and staff.role.name in ['Residence Assistant', 'Residence Director']:
                current_semester = Semester.objects.filter(is_current=True).first()  # Get the current semester
                if current_semester:
                    return qs.filter(dorm=staff.dorm, semester=current_semester)  # Filter by assigned dorm and current semester

        return qs.none()  # No access for other users

    def has_add_permission(self, request: HttpRequest, obj: Enrollment | None = None) -> bool:
        """Only superuser and ResLife Directors can add; Residence Directors can add for their assigned dorm."""
        if self._is_superuser(request) or self._is_reslife_director(request):
            return True
    
        if (self._is_residence_director(request) or self._is_residence_assistant(request)) and obj:
            staff = Staffs.objects.filter(user=request.user).first()
            return obj.dorm in StaffAssignment.objects.filter(staff=staff).values_list('dorm', flat=True)
        return False

    def has_change_permission(self, request: HttpRequest, obj: Enrollment | None = None) -> bool:
        """Only superuser and ResLife Directors can change; Residence Directors can change for their assigned dorm."""
        if self._is_superuser(request) or self._is_reslife_director(request):
            return True
        if (self._is_residence_director(request) or self._is_residence_assistant(request)) and obj:
            staff = Staffs.objects.filter(user=request.user).first()
            return obj.dorm in StaffAssignment.objects.filter(staff=staff).values_list('dorm', flat=True)
        return False
    
    def has_delete_permission(self, request: HttpRequest, obj: Enrollment | None = None) -> bool:
        """Only superuser and ResLife Directors can delete; Residence Directors can delete for their assigned dorm."""
        if self._is_superuser(request) or self._is_reslife_director(request):
            return True
        if self._is_residence_director(request) and obj:
            staff = Staffs.objects.filter(user=request.user).first()
            return obj.dorm in StaffAssignment.objects.filter(staff=staff).values_list('dorm', flat=True)
        return False

class StaffAssignmentAdmin(admin.ModelAdmin):
    list_display = ('id','staff', 'dorm', 'role', 'academic_session', 'semester')
    search_fields = (
        'staff__user__username', 'dorm__name', 
        'role__name', 'academic_session__name', 
        'semester__semester_type'
    )
    list_filter = ('dorm', 'role', 'academic_session', 'semester')
    ordering = ('academic_session', 'semester', 'dorm', 'staff')
    list_select_related = ('staff', 'dorm', 'role', 'academic_session', 'semester')
    autocomplete_fields = ('staff', 'dorm', 'role', 'academic_session', 'semester')

    def save_model(self, request, obj, form, change):
        obj.clean()  # Ensure validation is performed
        super().save_model(request, obj, form, change)

    def has_view_permission(self, request: HttpRequest, obj: StaffAssignment | None = None) -> bool:
        """Allows all staff members to view all staff assignments."""
        return request.user.is_authenticated and hasattr(request.user, 'staff')

    def has_add_permission(self, request: HttpRequest) -> bool:
        """Only superuser and ResLife Directors can add staff assignments."""
        return self._is_superuser(request) or self._is_reslife_director(request)

    def has_change_permission(self, request: HttpRequest, obj: StaffAssignment | None = None) -> bool:
        """Only superuser and ResLife Directors can change staff assignments."""
        return self._is_superuser(request) or self._is_reslife_director(request)

    def has_delete_permission(self, request: HttpRequest, obj: StaffAssignment | None = None) -> bool:
        """Only superuser and ResLife Directors can delete staff assignments."""
        return self._is_superuser(request) or self._is_reslife_director(request)

    def _is_superuser(self, request: HttpRequest) -> bool:
        """Checks if the user is a Django superuser."""
        return request.user.is_superuser

    def _is_reslife_director(self, request: HttpRequest) -> bool:
        """Checks if the user is a ResLife Director."""
        return request.user.is_authenticated and hasattr(request.user, 'staff') and request.user.staff.role.name == 'ResLife Directors'

    def get_queryset(self, request):
        """Customize the queryset based on the user's role."""
        qs = super().get_queryset(request)
        if self._is_superuser(request) or self._is_reslife_director(request):
            return qs  # Allow superusers and ResLife Directors to see all assignments
        elif request.user.is_authenticated and hasattr(request.user, 'staff'):
            return qs.filter(dorm__in=request.user.staff.dorms.all())  # Only show assignments for their assigned dorms
        return qs.none()  # No assignments for others

# Register StaffAssignmentAdmin
admin.site.register(StaffAssignment, StaffAssignmentAdmin)
