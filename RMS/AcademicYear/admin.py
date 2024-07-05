from django.contrib import admin
from .models import AcademicSession, Semester

@admin.register(AcademicSession)
class AcademicSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','start_year','end_year')
    search_fields = ('timeline',)

@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('id', 'semester_type', 'academic_session', 'start_date', 'end_date')
    list_filter = ('semester_type', 'academic_session__timeline')
    search_fields = ('semester_type', 'academic_session__timeline')
