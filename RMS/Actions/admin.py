from django.core.exceptions import ValidationError
from django.contrib import admin

from .models import MaintenanceRequest, Category, SubCategory, Announcement,Complaint

@admin.register(MaintenanceRequest)
class MaintenanceRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'resident', 'dorm', 'room', 'category', 'sub_category','description', 'status', 'created_at', 'updated_at', 'completion_date', 'updated_by']
    list_filter = ['status', 'category', 'sub_category', 'created_at', 'updated_at', 'completion_date']
    search_fields = ['id', 'resident__user__username', 'dorm__name', 'room__room_number', 'category', 'sub_category']
    readonly_fields = ['created_at', 'updated_at', 'completion_date']

    def save_model(self, request, obj, form, change):
        if change:  # If updating an existing object
            if 'status' in form.changed_data:
                staff_profile = request.user.staff_profile
                if not staff_profile:
                    raise ValidationError("Only staff can change the status.")
                if staff_profile.role.name not in ['Residence Assistant', 'Residence Director']:
                    raise ValidationError("Only staff with the role of Residence Assistant or Residence Director can change the status.")
                if staff_profile.dorm != obj.dorm:
                    raise ValidationError("Only staff assigned to the dorm can update the maintenance request.")
                obj.updated_by = staff_profile

        super().save_model(request, obj, form, change)
class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    extra = 1  # Number of empty subcategory forms to display

class CategoryAdmin(admin.ModelAdmin):
    inlines = [SubCategoryInline]
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_by', 'is_global', 'created_at',  'academic_session', 'semester','updated_at']
    list_filter = ['is_global', 'academic_session', 'semester', 'created_at', 'updated_at']
    search_fields = ['title', 'created_by__user__username']
    readonly_fields = ['created_at', 'updated_at']

    def save_model(self, request, obj, form, change):
        if not change:  # New announcement
            obj.created_by = request.user.staff_profile
        
        if obj.is_global:
            if obj.created_by.role.name != 'ResLife Director':
                raise ValidationError("Only ResLife Directors can make global announcements.")
        else:
            if not obj.dorms.exists():
                raise ValidationError("Announcements must be assigned to a dorm.")
            for dorm in obj.dorms.all():
                if obj.created_by.dorm != dorm and obj.created_by.role.name not in ['Residence Director', 'Residence Assistant']:
                    raise ValidationError("You can only create announcements for the dorm you are assigned to.")

        super().save_model(request, obj, form, change)

class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'is_anonymous', 'semester', 'academic_session', 'created_at')
    search_fields = ('user__username', 'description')
    list_filter = ('is_anonymous', 'semester', 'academic_session')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Only show anonymous complaints to ResLife Directors and Deans of Students Affairs
        if request.user.role.name in ['ResLife Director', 'Dean of Students Affairs']:
            return qs
        return qs.filter(is_anonymous=False)

    def has_view_permission(self, request, obj=None):
        # Allow staff with appropriate roles to view anonymous complaints
        if obj and obj.is_anonymous:
            return request.user.role.name in ['ResLife Director', 'Dean of Students Affairs']
        return super().has_view_permission(request, obj)

    def has_change_permission(self, request, obj=None):
        # Allow only ResLife Directors and Deans of Students Affairs to change anonymous complaints
        if obj and obj.is_anonymous:
            return request.user.role.name in ['ResLife Director', 'Dean of Students Affairs']
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        # Allow deletion based on roles
        return request.user.role.name in ['ResLife Director', 'Dean of Students Affairs']


admin.site.register(Complaint, ComplaintAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory)



