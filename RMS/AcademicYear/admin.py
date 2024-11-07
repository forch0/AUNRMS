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
    search_fields = ['resident__user__username', 'academic_session__name', 'semester__semester_type', 'dorm__name', 'room__room_number']

    def _is_superuser(self, request: HttpRequest) -> bool:
        """Checks if the user is a Django superuser."""
        return request.user.is_superuser

    def _is_reslife_director(self, request: HttpRequest) -> bool:
        """Checks if the user has the 'ResLife Director' role."""
        staff = Staffs.objects.filter(user=request.user).first()
        return staff and staff.role.name == 'ResLife Directors'

    def _is_dean_of_student_affairs(self, request: HttpRequest) -> bool:
        """Checks if the user has the 'Dean of Student Affairs' role."""
        staff = Staffs.objects.filter(user=request.user).first()
        return staff and staff.role.name == 'Dean of Student Affairs'

    def _is_resident(self, request: HttpRequest) -> bool:
        """Checks if the user is a resident."""
        return hasattr(request.user, 'resident')

    def _is_residence_assistant_or_director(self, request: HttpRequest) -> bool:
        """Checks if the user is a 'Residence Assistant' or 'Residence Director'."""
        staff = Staffs.objects.filter(user=request.user).first()
        return staff and staff.role.name in ['Residence Assistant', 'Residence Director']

    def has_view_permission(self, request: HttpRequest, obj: Enrollment | None = None) -> bool:
        """Allows superusers, residents, and specific roles to view enrollments."""
        if self._is_superuser(request) or self._is_reslife_director(request) or self._is_dean_of_student_affairs(request):
            return True

        if self._is_resident(request):
            return True

        if self._is_residence_assistant_or_director(request):
            return True

        return False

    def has_add_permission(self, request: HttpRequest) -> bool:
        """Allows superusers and specific roles to add enrollments."""
        # Restrict to superuser, ResLife Director, and Dean of Student Affairs
        return self._is_superuser(request) or self._is_reslife_director(request) or self._is_dean_of_student_affairs(request)

    def has_change_permission(self, request: HttpRequest, obj: Enrollment | None = None) -> bool:
        """Allows superusers and specific roles to change enrollments."""
        # Restrict to superuser, ResLife Director, Dean of Student Affairs, Residence Assistant, and Residence Director
        return (self._is_superuser(request) or self._is_reslife_director(request) or
                self._is_dean_of_student_affairs(request) or self._is_residence_assistant_or_director(request))

    def has_delete_permission(self, request: HttpRequest, obj: Enrollment | None = None) -> bool:
        """Allows only superusers and specific roles to delete enrollments."""
        # Restrict deletion to superuser and ResLife Director only
        return self._is_superuser(request) or self._is_reslife_director(request)

    def get_queryset(self, request: HttpRequest):
        """
        Restricts the queryset based on user roles and assignments.
        """
        qs = super().get_queryset(request)
        
        if self._is_superuser(request) or self._is_reslife_director(request) or self._is_dean_of_student_affairs(request):
            return qs  # Superusers, ResLife Directors, and Deans see all

        # For residents, filter to their enrollments only
        if self._is_resident(request):
            return qs.filter(resident=request.user.resident)

        # For Residence Assistant and Residence Director, filter by assigned dorm and current semester
        if self._is_residence_assistant_or_director(request):
            current_semester = Semester.objects.filter(is_current=True).first()
            if current_semester:
                return qs.filter(dorm__in=self._assigned_dorms(request), semester=current_semester)

        return qs.none()  # No access for other users

class StaffAssignmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'staff', 'dorm', 'role', 'academic_session', 'semester')
    search_fields = (
        'staff__user__username', 'dorm__name', 
        'role__name', 'academic_session__name', 
        'semester__semester_type'
    )
    list_filter = ('dorm', 'role', 'academic_session', 'semester')
    ordering = ('academic_session', 'semester', 'dorm', 'staff')
    list_select_related = ('staff', 'dorm', 'role', 'academic_session', 'semester')
    autocomplete_fields = ('staff', 'dorm', 'role', 'academic_session', 'semester')

    def _is_superuser(self, request: HttpRequest) -> bool:
        """Checks if the user is a Django superuser."""
        return request.user.is_superuser

    def _is_reslife_director(self, request: HttpRequest) -> bool:
        """Checks if the user has the 'ResLife Director' role."""
        staff = Staffs.objects.filter(user=request.user).first()
        return staff and staff.role.name == 'ResLife Directors'

    def _is_dean_of_student_affairs(self, request: HttpRequest) -> bool:
        """Checks if the user has the 'Dean of Student Affairs' role."""
        staff = Staffs.objects.filter(user=request.user).first()
        return staff and staff.role.name == 'Dean of Student Affairs'

    def _is_residence_assistant(self, request: HttpRequest) -> bool:
        """Checks if the user has the 'Residence Assistant' role."""
        staff = Staffs.objects.filter(user=request.user).first()
        return staff and staff.role.name == 'Residence Assistant'

    def _is_residence_director(self, request: HttpRequest) -> bool:
        """Checks if the user has the 'Residence Director' role."""
        staff = Staffs.objects.filter(user=request.user).first()
        return staff and staff.role.name == 'Residence Director'

    def has_view_permission(self, request: HttpRequest, obj=None) -> bool:
        """Allows superusers, ResLife Directors, Deans of Student Affairs, Residence Assistants, and Residence Directors to view assignments."""
        if self._is_superuser(request):
            return True
        if self._is_reslife_director(request):
            return True
        if self._is_dean_of_student_affairs(request):
            return True
        if self._is_residence_assistant(request):
            # RAs can only view assignments in their dorm
            staff = Staffs.objects.filter(user=request.user).first()
            if staff and obj and obj.dorm == staff.dorm:
                return True
        if self._is_residence_director(request):
            # Residence Directors can view assignments for their dorm
            staff = Staffs.objects.filter(user=request.user).first()
            if staff and obj and obj.dorm == staff.dorm:
                return True
        return False

    def has_add_permission(self, request: HttpRequest) -> bool:
        """Allows only superusers, ResLife Directors, and Residence Directors to add assignments."""
        if self._is_superuser(request):
            return True
        if self._is_reslife_director(request):
            return True
        if self._is_residence_director(request):
            return True
        return False

    def has_change_permission(self, request: HttpRequest, obj=None) -> bool:
        """Allows superusers, ResLife Directors, Residence Directors, and Deans of Student Affairs to change assignments."""
        if self._is_superuser(request):
            return True
        if self._is_reslife_director(request):
            return True
        if self._is_dean_of_student_affairs(request):
            return True
        if self._is_residence_director(request):
            # Residence Directors can change assignments only in their dorm
            staff = Staffs.objects.filter(user=request.user).first()
            if staff and obj and obj.dorm == staff.dorm:
                return True
        return False

    def has_delete_permission(self, request: HttpRequest, obj=None) -> bool:
        """Allows only superusers, ResLife Directors, and Residence Directors to delete assignments."""
        if self._is_superuser(request):
            return True
        if self._is_reslife_director(request):
            return True
        if self._is_residence_director(request):
            # Residence Directors can delete assignments in their dorm
            staff = Staffs.objects.filter(user=request.user).first()
            if staff and obj and obj.dorm == staff.dorm:
                return True
        return False

# Register StaffAssignmentAdmin
admin.site.register(StaffAssignment, StaffAssignmentAdmin)
