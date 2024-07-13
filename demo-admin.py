from django.contrib import admin
from .models import AcademicSession, Semester, MaintenanceRequest, Complaint, Announcement

@admin.register(AcademicSession)
class AcademicSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'start_year', 'end_year', 'name')
    list_filter = ('start_year', 'end_year')
    search_fields = ('name',)

@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('id', 'semester_type', 'start_date', 'end_date', 'academic_session')
    list_filter = ('semester_type', 'start_date', 'end_date', 'academic_session')
    search_fields = ('semester_type', 'academic_session__name')

@admin.register(MaintenanceRequest)
class MaintenanceRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'status', 'created_at', 'updated_at', 'resolved_at', 'academic_session', 'semester')
    list_filter = ('status', 'created_at', 'updated_at', 'resolved_at', 'academic_session', 'semester')
    search_fields = ('title', 'description', 'user__username', 'academic_session__name', 'semester__semester_type')
    fieldsets = (
        (None, {
            'fields': ('user', 'title', 'description', 'status', 'academic_session', 'semester')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'resolved_at')
        }),
    )
    readonly_fields = ('created_at', 'updated_at', 'resolved_at')

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'anonymous', 'created_at', 'academic_session', 'semester')
    list_filter = ('anonymous', 'created_at', 'academic_session', 'semester')
    search_fields = ('title', 'description', 'user__username', 'academic_session__name', 'semester__semester_type')
    fieldsets = (
        (None, {
            'fields': ('user', 'title', 'description', 'anonymous', 'academic_session', 'semester')
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )
    readonly_fields = ('created_at',)

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at', 'updated_at', 'active', 'academic_session', 'semester')
    list_filter = ('active', 'created_at', 'updated_at', 'academic_session', 'semester')
    search_fields = ('title', 'content', 'academic_session__name', 'semester__semester_type')
    fieldsets = (
        (None, {
            'fields': ('title', 'content', 'active', 'academic_session', 'semester')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    readonly_fields = ('created_at', 'updated_at')
