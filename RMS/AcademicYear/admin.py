from django.contrib import admin
from .models import AcademicSession, Semester, Enrollment, StaffAssignment


@admin.register(AcademicSession)
class AcademicSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'start_year', 'end_year')
    search_fields = ('name', 'start_year', 'end_year')
    ordering = ('start_year',)

    

@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('id', 'semester_type', 'start_date', 'end_date', 'academic_session')
    list_filter = ('semester_type', 'academic_session')
    search_fields = ('semester_type', 'academic_session__name')
    ordering = ('start_date',)

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'resident', 'semester', 'academic_session', 'dorm', 'room', 'date_enrolled')
    list_filter = ('semester', 'academic_session', 'dorm', 'room')
    search_fields = ('resident__user__username', 'dorm__name', 'room__number')
    ordering = ('date_enrolled',)

class StaffAssignmentAdmin(admin.ModelAdmin):
    list_display = ('staff', 'dorm', 'role', 'academic_session', 'semester')
    search_fields = ('staff__user__username', 'dorm__name', 'role__name', 'academic_session__name', 'semester__semester_type')
    list_filter = ('dorm', 'role', 'academic_session', 'semester')
    ordering = ('academic_session', 'semester', 'dorm', 'staff')
    list_select_related = ('staff', 'dorm', 'role', 'academic_session', 'semester')
    autocomplete_fields = ('staff', 'dorm', 'academic_session', 'semester')

    def save_model(self, request, obj, form, change):
        obj.clean()  # Ensure validation is performed
        super().save_model(request, obj, form, change)

admin.site.register(StaffAssignment, StaffAssignmentAdmin)
