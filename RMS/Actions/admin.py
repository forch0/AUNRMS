from django.core.exceptions import ValidationError
from django.contrib import admin

from .models import MaintenanceRequest, Category, SubCategory, Announcement, Complaint

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
    list_display = ('id', 'title', 'created_by', 'created_at', 'is_global')
    list_filter = ('is_global', 'academic_session', 'semester')
    search_fields = ('title', 'created_by__user__username', 'academic_session__name')
    ordering = ('created_at',)

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'enrollment', 'semester', 'academic_session', 'is_anonymous')
    list_filter = ('semester', 'academic_session', 'is_anonymous')
    search_fields = ('user__username', 'description')
    # ordering = ('created_at',)
    
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory)



