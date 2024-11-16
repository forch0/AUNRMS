from django.core.exceptions import ValidationError
from django.contrib import admin
from django.http import HttpResponse
from .models import MaintenanceRequest, Category, SubCategory, Announcement, Complaint, Vendor
from adminsortable2.admin import SortableAdminMixin
from .forms import ComplaintForm
from UserProfiles.models import Staffs
from AcademicYear.models import Enrollment
from django.http import HttpRequest
from import_export import resources
from import_export.admin import ExportMixin
from import_export.formats.base_formats import XLSX
@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_by', 'created_at', 'is_global')
    list_filter = ('is_global', 'academic_session', 'semester')
    search_fields = ('title', 'created_by__user__username', 'academic_session__name')
    ordering = ('created_at',)

    def _is_reslife_directors(self, request: HttpRequest) -> bool:
        """Checks if the user is a ResLife Director."""
        staff = Staffs.objects.filter(user=request.user).first()
        return staff and staff.role.name == 'ResLife Directors'

    def has_view_permission(self, request: HttpRequest, obj: Announcement | None = None) -> bool:
        if request.user.is_superuser or self._is_reslife_directors:
            return True  # Superusers can view all announcements

        # Allow all staff to view global announcements
        if request.user.is_staff:
            if obj and obj.is_global:
                return True

        # Allow residents to view global announcements
        if hasattr(request.user, 'resident'):
            if obj and obj.is_global:
                return True
            
            staff = Staffs.objects.filter(user=request.user).first()
            if staff:
                # Allow Residence Directors and Assistants to view announcements for their assigned dorms
                return obj and obj.dorm in staff.staffassignment_set.values_list('dorm', flat=True)

        # Allow residents to view announcements for their dorm
        if hasattr(request.user, 'resident'):
            enrollments = Enrollment.objects.filter(resident__user=request.user)
            assigned_dorms = enrollments.values_list('dorm', flat=True)
            if obj and obj.dorm in assigned_dorms:
                return True  # Residents can see announcements for their dorm

        return False  # No access for anyone else

    def has_add_permission(self, request: HttpRequest) -> bool:
        """Restrict add permission based on user roles."""
        if request.user.is_superuser or self._is_reslife_directors:
            return True  # Superusers can add any announcement

        staff = Staffs.objects.filter(user=request.user).first()
        if staff and staff.role.name == 'Residence Director' or 'Residence Assistant' :
            return True  # Residence Directors can create announcements for their dorms
        return False  # Deny add permissions for everyone else
    
    def save_model(self, request, obj: Announcement, form, change):
        """Override save_model to set the created_by field."""
        if not change:  # If the announcement is new
            staff = Staffs.objects.filter(user=request.user).first()
            if staff:
                obj.created_by = staff  # Set the creator of the announcement
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request: HttpRequest):
        """Filter the queryset based on user roles."""
        queryset = super().get_queryset(request)

        if request.user.is_superuser or self._is_reslife_directors:
            return queryset  # Superusers see everything

        staff = Staffs.objects.filter(user=request.user).first()
        if staff:
            # Allow Residence Directors and Residence Assistants to see announcements for their assigned dorms
            return queryset.filter(dorm__in=staff.staffassignment_set.values_list('dorm', flat=True))

        if hasattr(request.user, 'resident'):
            # Allow residents to see announcements for their dorm
            enrollments = Enrollment.objects.filter(resident__user=request.user)
            assigned_dorms = enrollments.values_list('dorm', flat=True)
            return queryset.filter(dorm__in=assigned_dorms)

        return queryset.none()
    
    def has_change_permission(self, request: HttpRequest, obj: Announcement | None = None) -> bool:
        """Allow only authorized staff to update announcements."""
        if request.user.is_superuser or self._is_reslife_directors:
            return True  # Superuser can update anything

        staff = Staffs.objects.filter(user=request.user).first()
        if staff and staff.role.name in ['Residence Director', 'Residence Assistant']:
            # Allow staff to change announcements for their assigned dorm
            return obj and obj.dorm in staff.staffassignment_set.values_list('dorm', flat=True)
        return False  # Deny access otherwise  # No access for anyone else

    def has_delete_permission(self, request: HttpRequest, obj: Announcement | None = None) -> bool:
        """Allow only superusers and Residence Directors to delete announcements."""
        if request.user.is_superuser or self._is_reslife_directors:
            return True  # Superuser can delete anything

        staff = Staffs.objects.filter(user=request.user).first()
        if staff and staff.role.name == 'Residence Director':
            # Allow Residence Directors to delete announcements for their dorm
            return obj and obj.dorm in staff.staffassignment_set.values_list('dorm', flat=True)
        return False  # Deny access otherwise
 # No delete permission otherwise

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'complaint_type', 'created_at', 'is_anonymous', 'semester', 'academic_session')
    list_filter = ('complaint_type', 'semester', 'academic_session', 'is_anonymous')
    search_fields = (
        'description', 'user__username', 'semester__name', 'academic_session__name',
        'enrollment__student__user__username'
    )
    ordering = ('created_at',)
    autocomplete_fields = ('user', 'semester', 'academic_session', 'enrollment')  # Related fields for autocomplete

    def _is_reslife_directors(self, request: HttpRequest) -> bool:
        """Checks if the user is a ResLife Director."""
        staff = Staffs.objects.filter(user=request.user).first()
        return staff and staff.role.name == 'ResLife Directors'

    def has_view_permission(self, request: HttpRequest, obj: Complaint | None = None) -> bool:
        if request.user.is_superuser or self._is_reslife_directors(request):
            return True  # Superusers and ResLife Directors can view all complaints

        # Allow all staff to view complaints in certain statuses (e.g., 'Pending' or 'Resolved')
        if request.user.is_staff:
            if obj and obj.status in ['Pending', 'Resolved']:  # Modify status based on your needs
                return True

        # Allow residents to view their own complaints
        if hasattr(request.user, 'resident'):
            if obj and obj.resident.user == request.user:
                return True  # Resident can view their own complaint

        return False  # No access otherwise

    def has_add_permission(self, request: HttpRequest) -> bool:
        """Restrict add permission based on user roles."""
        if request.user.is_superuser or self._is_reslife_directors(request):
            return True  # Superusers and ResLife Directors can add any complaint

        staff = Staffs.objects.filter(user=request.user).first()
        if staff and staff.role.name in ['Residence Director', 'Residence Assistant']:
            return True  # Residence Directors and Assistants can add complaints for their dorms
        return False  # Deny add permissions for everyone else

    def save_model(self, request, obj: Complaint, form, change):
        """Override save_model to set the created_by field."""
        if not change:  # If the complaint is new
            staff = Staffs.objects.filter(user=request.user).first()
            if staff:
                obj.created_by = staff  # Set the creator of the complaint
        super().save_model(request, obj, form, change)

    def get_queryset(self, request: HttpRequest):
        """Filter the queryset based on user roles."""
        queryset = super().get_queryset(request)

        if request.user.is_superuser or self._is_reslife_directors(request):
            return queryset  # Superusers see everything

        staff = Staffs.objects.filter(user=request.user).first()
        if staff:
            # Allow Residence Directors and Residence Assistants to see complaints for their assigned dorms
            return queryset.filter(dorm__in=staff.staffassignment_set.values_list('dorm', flat=True))

        if hasattr(request.user, 'resident'):
            # Allow residents to see their own complaints
            return queryset.filter(resident__user=request.user)

        return queryset.none()

    def has_change_permission(self, request: HttpRequest, obj: Complaint | None = None) -> bool:
        """Allow only authorized staff to update complaints."""
        if request.user.is_superuser or self._is_reslife_directors(request):
            return True  # Superusers and ResLife Directors can change any complaint

        staff = Staffs.objects.filter(user=request.user).first()
        if staff and staff.role.name in ['Residence Director', 'Residence Assistant']:
            # Allow staff to change complaints for their assigned dorm
            return obj and obj.dorm in staff.staffassignment_set.values_list('dorm', flat=True)
        return False  # Deny access otherwise

    def has_delete_permission(self, request: HttpRequest, obj: Complaint | None = None) -> bool:
        """Allow only superusers and Residence Directors to delete complaints."""
        if request.user.is_superuser or self._is_reslife_directors(request):
            return True  # Superusers and ResLife Directors can delete any complaint

        staff = Staffs.objects.filter(user=request.user).first()
        if staff and staff.role.name == 'Residence Director':
            # Allow Residence Directors to delete complaints for their dorm
            return obj and obj.dorm in staff.staffassignment_set.values_list('dorm', flat=True)
        return False  # Deny access otherwise



class MaintenanceRequestsResource(resources.ModelResource):
    class Meta:
        model = MaintenanceRequest
@admin.register(MaintenanceRequest)
class MaintenanceRequestAdmin(ExportMixin,admin.ModelAdmin):
    list_display = [
        'id', 'resident', 'dorm', 'room', 
        'category','sub_category', 'description', 
        'status', 'created_at', 'updated_at', 
        'completion_date', 'updated_by','semester', 'academic_session'
    ]
    
    # Search fields mapped to fields in the model and foreign keys
    search_fields = [
        'id',                      # UUID of the request
        'resident__user__email',    # Resident's email through the user model
        'dorm__name',               # Dorm name
        'room__room_number',        # Room number
        'category__name',           # Category name
        'sub_category__name',       # Subcategory name
        'updated_by__user__email',
        'academic_session__name', 
        'semester__semester_type',   # Updated by staff's email through the user model
    ]
    
    list_filter = ['status', 'category', 'sub_category', 'created_at', 'updated_at', 'completion_date']
    readonly_fields = ['created_at', 'updated_at', 'completion_date']
    ordering = ['created_at', 'dorm', 'resident']
    
    # Optimizing database queries by prefetching related models
    list_select_related = [
        'resident', 'dorm', 'room', 'category', 'sub_category', 'updated_by','semester', 'academic_session'
    ]
    
    # Autocomplete fields for foreign keys
    autocomplete_fields = (
        'resident', 'dorm', 'room', 'category','semester', 'academic_session'
    )
    
    resource_class = MaintenanceRequestsResource


    def export_selected(self, request, queryset):
        dataset = MaintenanceRequestsResource().export(queryset=queryset)
        response = HttpResponse(dataset.xlsx, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="maintenance_requests.xlsx"'
        return response
    
    export_selected.short_description = "Export selected maintenance requests to XLSX"
    actions = ['export_selected']


    def _is_staff_assigned_to_dorm(self, request: HttpRequest, obj: MaintenanceRequest) -> bool:
        """Check if the staff is assigned to the dorm for the semester and session."""
        staff = Staffs.objects.filter(user=request.user).first()
        if not staff:
            return False  # No valid staff record

        return staff.staffassignment_set.filter(
            dorm=obj.dorm, semester=obj.semester, academic_session=obj.academic_session
        ).exists()
    
    def get_queryset(self, request: HttpRequest):
        """Filter the queryset based on the user’s role and dorm assignment."""
        queryset = super().get_queryset(request)

        if request.user.is_superuser:
            return queryset  # Superusers see everything

        staff = Staffs.objects.filter(user=request.user).first()
        if staff:
            if staff.role.name in ['ResLife Director', 'Dean of Student Affairs']:
                return queryset  # Directors and Deans see all requests

            # Filter requests by the staff’s assigned dorms for the current semester/session
            assigned_dorms = staff.staffassignment_set.values_list('dorm', flat=True)
            return queryset.filter(dorm__in=assigned_dorms)

        if hasattr(request.user, 'resident'):
            # Residents see only their own requests
            return queryset.filter(resident__user=request.user)

        return queryset.none()  # No access for anyone else

    def has_view_permission(self, request: HttpRequest, obj: MaintenanceRequest | None = None) -> bool:
        """Define view permissions."""
        if request.user.is_superuser:
            return True

        staff = Staffs.objects.filter(user=request.user).first()
        if staff:
            if staff.role.name in ['ResLife Directors', 'Dean of Student Affairs']:
                return True  # Can view all requests

            if obj and self._is_staff_assigned_to_dorm(request, obj):
                return True  # Assigned staff can view requests in their dorm

        if hasattr(request.user, 'resident'):
            return obj is None or obj.resident.user == request.user  # Residents see their own requests
        return False

    def has_add_permission(self, request: HttpRequest) -> bool:
        """Restrict add permission based on user roles and assignments."""
        if request.user.is_superuser:
            return True  # Superusers can add any request

        staff = Staffs.objects.filter(user=request.user).first()
        if staff:
            if staff.role.name == 'ResLife Directors':
                return True  # ResLife Directors can create requests

            # Check if the staff is assigned to a dorm for the semester
            assigned_dorms = staff.staffassignment_set.values_list('dorm', flat=True)
            if assigned_dorms.exists():
                return True  # Assigned staff can create requests for their dorm

        # Allow residents to create requests for their dorm
        if hasattr(request.user, 'resident'):
            return True  # Residents can add maintenance requests

        return False  # Deny add permissions for everyone else
    
    def has_change_permission(self, request: HttpRequest, obj: MaintenanceRequest | None = None) -> bool:
        """Allow only authorized staff to update requests."""
        if request.user.is_superuser:
            return True  # Superuser can update anything

        staff = Staffs.objects.filter(user=request.user).first()
        if staff and staff.role.name in ['ResLife Directors', 'Dean of Student Affairs']:
            return True  # ResLife Directors and Dean can update all requests

        # Check if the staff is assigned to the dorm
        if obj and self._is_staff_assigned_to_dorm(request, obj):
            if staff.role.name in ['Residence Assistant', 'Residence Director']:
                return True  # Assigned staff can update requests in their dorm

        return False  # Deny access otherwise
    
    def has_delete_permission(self, request: HttpRequest, obj: MaintenanceRequest | None = None) -> bool:
        """Allow only superusers and ResLife Directors to delete requests."""
        if request.user.is_superuser:
            return True  # Superuser can delete anything

        staff = Staffs.objects.filter(user=request.user).first()
        if staff and staff.role.name in ['ResLife Directors', 'Dean of Student Affairs']:
            return True  # ResLife Directors and Dean can update all requests

        # Check if the staff is assigned to the dorm
        if obj and self._is_staff_assigned_to_dorm(request, obj):
            if staff.role.name in ['Residence Assistant', 'Residence Director']:
                return True  # Assigned staff can delete requests in their dorm

        return False  # Deny access otherwise

class SubCategoryInline(SortableAdminMixin,admin.TabularInline):
    list_display = ('name','my_order','category')
    search_fields = ('name','category')
    model = SubCategory
    extra = 1  # Number of empty subcategory forms to display
    ordering = ['my_order']

    autocomplete_fields = (
       'category',
    )
    

    def _is_reslife_directors(self, request: HttpRequest) -> bool:
        """Checks if the user is a ResLife Director."""
        staff = Staffs.objects.filter(user=request.user).first()
        return staff and staff.role.name == 'ResLife Directors'

    # Overriding has_view_permission to allow viewing for superusers and ResLife Directors
    def has_view_permission(self, request: HttpRequest, obj: Category | None = None) -> bool:
        if request.user.is_superuser or self._is_reslife_directors(request):
            return True  # Superusers and ResLife Directors can view categories
        return False  # All others are restricted from viewing

    # Overriding has_add_permission to allow adding for superusers and ResLife Directors
    def has_add_permission(self, request: HttpRequest) -> bool:
        if request.user.is_superuser or self._is_reslife_directors(request):
            return True  # Superusers and ResLife Directors can add categories
        return False  # All others are restricted from adding

    # Overriding has_change_permission to allow changing for superusers and ResLife Directors
    def has_change_permission(self, request: HttpRequest, obj: Category | None = None) -> bool:
        if request.user.is_superuser or self._is_reslife_directors(request):
            return True  # Superusers and ResLife Directors can change categories
        return False  # All others are restricted from changing

    # Overriding has_delete_permission to allow deleting for superusers and ResLife Directors
    def has_delete_permission(self, request: HttpRequest, obj: Category | None = None) -> bool:
        if request.user.is_superuser or self._is_reslife_directors(request):
            return True  # Superusers and ResLife Directors can delete categories
        return False  # All others are restricted from deleting
class CategoryAdmin(SortableAdminMixin,admin.ModelAdmin):
    inlines = [SubCategoryInline]
    list_display = ('name','my_order')
    search_fields = ('name',)
    ordering = ['my_order']

    # Helper function to check if the user is a ResLife Director
    def _is_reslife_directors(self, request: HttpRequest) -> bool:
        """Checks if the user is a ResLife Director."""
        staff = Staffs.objects.filter(user=request.user).first()
        return staff and staff.role.name == 'ResLife Directors'

    # Overriding has_view_permission to allow viewing for superusers and ResLife Directors
    def has_view_permission(self, request: HttpRequest, obj: Category | None = None) -> bool:
        if request.user.is_superuser or self._is_reslife_directors(request):
            return True  # Superusers and ResLife Directors can view categories
        return False  # All others are restricted from viewing

    # Overriding has_add_permission to allow adding for superusers and ResLife Directors
    def has_add_permission(self, request: HttpRequest) -> bool:
        if request.user.is_superuser or self._is_reslife_directors(request):
            return True  # Superusers and ResLife Directors can add categories
        return False  # All others are restricted from adding

    # Overriding has_change_permission to allow changing for superusers and ResLife Directors
    def has_change_permission(self, request: HttpRequest, obj: Category | None = None) -> bool:
        if request.user.is_superuser or self._is_reslife_directors(request):
            return True  # Superusers and ResLife Directors can change categories
        return False  # All others are restricted from changing

    # Overriding has_delete_permission to allow deleting for superusers and ResLife Directors
    def has_delete_permission(self, request: HttpRequest, obj: Category | None = None) -> bool:
        if request.user.is_superuser or self._is_reslife_directors(request):
            return True  # Superusers and ResLife Directors can delete categories
        return False  # All others are restricted from deleting
class VendorAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'owner_name', 'phone_number', 'dorm', 'is_off_campus', 'product')
    search_fields = ('business_name', 'owner_name', 'product')
    list_filter = ('dorm', 'is_off_campus')

    def _is_reslife_directors(self, request: HttpRequest) -> bool:
        """Checks if the user is a ResLife Director."""
        staff = Staffs.objects.filter(user=request.user).first()
        return staff and staff.role.name == 'ResLife Directors'

    # Overriding has_view_permission to allow viewing for superusers and ResLife Directors
    def has_view_permission(self, request: HttpRequest, obj: Category | None = None) -> bool:
        if request.user.is_superuser or self._is_reslife_directors(request):
            return True  # Superusers and ResLife Directors can view categories
        return False  # All others are restricted from viewing

    # Overriding has_add_permission to allow adding for superusers and ResLife Directors
    def has_add_permission(self, request: HttpRequest) -> bool:
        if request.user.is_superuser or self._is_reslife_directors(request):
            return True  # Superusers and ResLife Directors can add categories
        return False  # All others are restricted from adding

    # Overriding has_change_permission to allow changing for superusers and ResLife Directors
    def has_change_permission(self, request: HttpRequest, obj: Category | None = None) -> bool:
        if request.user.is_superuser or self._is_reslife_directors(request):
            return True  # Superusers and ResLife Directors can change categories
        return False  # All others are restricted from changing

    # Overriding has_delete_permission to allow deleting for superusers and ResLife Directors
    def has_delete_permission(self, request: HttpRequest, obj: Category | None = None) -> bool:
        if request.user.is_superuser or self._is_reslife_directors(request):
            return True  # Superusers and ResLife Directors can delete categories
        return False  # All others are restricted from deleting

    
admin.site.register(Vendor, VendorAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory)



