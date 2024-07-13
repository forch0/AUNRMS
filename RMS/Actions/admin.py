from django.contrib import admin
from .models import Announcement, Complaint

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'user', 'content', 'created_at', 'updated_at', 'active', 'academic_session', 'semester', 'global_announcement', 'dorm']
    list_filter = ['active', 'academic_session', 'semester', 'global_announcement']
    search_fields = ['title', 'content']
    date_hierarchy = 'created_at'


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'user', 'description', 'anonymous', 'created_at', 'academic_session', 'semester']
    list_filter = ['anonymous', 'academic_session', 'semester']
    search_fields = ['title', 'description']
    date_hierarchy = 'created_at'
