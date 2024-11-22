from django.core.exceptions import PermissionDenied
from django.core.exceptions import ValidationError
from django.contrib import admin
from django.http import HttpResponse
from .models import MaintenanceRequest, Category, SubCategory, Announcement, Complaint, Vendor
from adminsortable2.admin import SortableAdminMixin
from .forms import ComplaintForm, AnnouncementForm
from UserProfiles.models import Staffs
from Dorms.models import Dorm, Room
from AcademicYear.models import *
from UserProfiles.models import *
from django.http import HttpRequest
from import_export.widgets import ForeignKeyWidget, DateWidget
from import_export import resources,fields
from import_export.admin import ExportMixin
from import_export.formats.base_formats import XLSX
from django.utils.dateformat import DateFormat
# @admin.register(Announcement)
# class AnnouncementAdmin(admin.ModelAdmin):
#     list_display = ('id', 'title', 'created_by', 'created_at', 'is_global')
#     list_filter = ('is_global', 'academic_session', 'semester')
#     search_fields = ('title', 'created_by__user__username', 'academic_session__name')
#     ordering = ('created_at',)

#     def _is_reslife_directors(self, request: HttpRequest) -> bool:
#         """Checks if the user is a ResLife Director."""
#         staff = Staffs.objects.filter(user=request.user).first()
#         return staff and staff.role.name == 'ResLife Directors'

#     def has_view_permission(self, request: HttpRequest, obj: Announcement | None = None) -> bool:
#         if request.user.is_superuser or self._is_reslife_directors:
#             return True  # Superusers can view all announcements

#         # Allow all staff to view global announcements
#         if request.user.is_staff:
#             if obj and obj.is_global:
#                 return True

#         # Allow residents to view global announcements
#         if hasattr(request.user, 'resident'):
#             if obj and obj.is_global:
#                 return True
            
#             staff = Staffs.objects.filter(user=request.user).first()
#             if staff:
#                 # Allow Residence Directors and Assistants to view announcements for their assigned dorms
#                 return obj and obj.dorm in staff.staffassignment_set.values_list('dorm', flat=True)

#         # Allow residents to view announcements for their dorm
#         if hasattr(request.user, 'resident'):
#             enrollments = Enrollment.objects.filter(resident__user=request.user)
#             assigned_dorms = enrollments.values_list('dorm', flat=True)
#             if obj and obj.dorm in assigned_dorms:
#                 return True  # Residents can see announcements for their dorm

#         return False  # No access for anyone else

#     def has_add_permission(self, request: HttpRequest) -> bool:
#         """Restrict add permission based on user roles."""
#         if request.user.is_superuser or self._is_reslife_directors:
#             return True  # Superusers can add any announcement

#         staff = Staffs.objects.filter(user=request.user).first()
#         if staff and staff.role.name == 'Residence Director' or 'Residence Assistant' :
#             return True  # Residence Directors can create announcements for their dorms
#         return False  # Deny add permissions for everyone else
    
#     def save_model(self, request, obj: Announcement, form, change):
#         """Override save_model to set the created_by field."""
#         if not change:  # If the announcement is new
#             staff = Staffs.objects.filter(user=request.user).first()
#             if staff:
#                 obj.created_by = staff  # Set the creator of the announcement
#         super().save_model(request, obj, form, change)
    
#     def get_queryset(self, request: HttpRequest):
#         """Filter the queryset based on user roles."""
#         queryset = super().get_queryset(request)

#         if request.user.is_superuser or self._is_reslife_directors:
#             return queryset  # Superusers see everything

#         staff = Staffs.objects.filter(user=request.user).first()
#         if staff:
#             # Allow Residence Directors and Residence Assistants to see announcements for their assigned dorms
#             return queryset.filter(dorm__in=staff.staffassignment_set.values_list('dorm', flat=True))

#         if hasattr(request.user, 'resident'):
#             # Allow residents to see announcements for their dorm
#             enrollments = Enrollment.objects.filter(resident__user=request.user)
#             assigned_dorms = enrollments.values_list('dorm', flat=True)
#             return queryset.filter(dorm__in=assigned_dorms)

#         return queryset.none()
    
#     def has_change_permission(self, request: HttpRequest, obj: Announcement | None = None) -> bool:
#         """Allow only authorized staff to update announcements."""
#         if request.user.is_superuser or self._is_reslife_directors:
#             return True  # Superuser can update anything

#         staff = Staffs.objects.filter(user=request.user).first()
#         if staff and staff.role.name in ['Residence Director', 'Residence Assistant']:
#             # Allow staff to change announcements for their assigned dorm
#             return obj and obj.dorm in staff.staffassignment_set.values_list('dorm', flat=True)
#         return False  # Deny access otherwise  # No access for anyone else

#     def has_delete_permission(self, request: HttpRequest, obj: Announcement | None = None) -> bool:
#         """Allow only superusers and Residence Directors to delete announcements."""
#         if request.user.is_superuser or self._is_reslife_directors:
#             return True  # Superuser can delete anything

#         staff = Staffs.objects.filter(user=request.user).first()
#         if staff and staff.role.name == 'Residence Director':
#             # Allow Residence Directors to delete announcements for their dorm
#             return obj and obj.dorm in staff.staffassignment_set.values_list('dorm', flat=True)
#         return False  # Deny access otherwise
 # No delete permission otherwise

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    form = AnnouncementForm
    list_display = ('title','message', 'created_by', 'is_global', 'semester', 'academic_session', 'created_at')
    list_filter = ('is_global', 'semester', 'academic_session', 'created_at')
    search_fields = ('title', 'message', 'created_by__email', 'created_by__name')
    ordering = ('-created_at',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        if request.user.is_superuser:
            return queryset

        # Check if the logged-in user has a staff profile
        staff_profile = getattr(request.user, 'staffs', None)
        if staff_profile:
            # Check if the staff role is 'ResLife Director'
            if staff_profile.role.name == 'ResLife Directors':
                return queryset  # ResLife Directors can view all announcements
            else:
                # Filter announcements by dorms assigned to the staff
                assigned_dorms = Dorm.objects.filter(staffassignment__staff=staff_profile)
                return queryset.filter(dorms__in=assigned_dorms).distinct()

        return queryset.none()  # If not staff, return an empty queryset

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        
        # Ensure 'created_by' is the current staff member
        if 'created_by' in form.base_fields:
            form.base_fields['created_by'].queryset = UserCred.objects.filter(id=request.user.id)

        # Limit dorms to the ones the current staff is assigned to
        if not request.user.is_superuser:
            staff_profile = getattr(request.user, 'staffs', None)
            if staff_profile:
                assigned_dorms = Dorm.objects.filter(staffassignment__staff=staff_profile)
                if 'dorms' in form.base_fields:
                    form.base_fields['dorms'].queryset = assigned_dorms

        # Make fields read-only if it's a view (GET request)
        if obj is not None:  # If we are viewing an existing object
            if 'dorms' in form.base_fields:
                form.base_fields['dorms'].disabled = True  # Disable dorms field when viewing
            # if 'created_by' in form.base_fields:
            #     form.base_fields['created_by'].disabled = True  # Disable created_by when viewing

        return form

    def save_model(self, request, obj, form, change):
    # Ensure the 'created_by' is assigned properly by the form
        super().save_model(request, obj, form, change)

    def has_add_permission(self, request):
        # Superusers always have add permissions
        if request.user.is_superuser:
            return True

        # Ensure the user has a staff profile
        staff_profile = getattr(request.user, 'staffs', None)
        if not staff_profile:
            return False  # Non-staff users cannot add announcements

        # Check the staff's role
        if staff_profile.role.name == 'ResLife Directors':
            return True  # ResLife Directors can add global announcements

        # Other staff can only add announcements for their assigned dorms
        assigned_dorms = Dorm.objects.filter(staffassignment__staff=staff_profile)
        return assigned_dorms.exists()  # Allow adding if the staff is assigned to any dorm

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is None:
            return True
        if hasattr(request.user, 'staffs'):
            staff_profile = request.user.staffs
            
            # Access the reverse relation using the updated related_name 'staffassignments'
            staff_assignments = staff_profile.staffassignments.all()  # Updated relation name
            
            # Get the assigned dorms for the staff
            assigned_dorms = staff_assignments.values_list('dorm__id', flat=True)

            # Check if the current object is assigned to the staff's dorms
            if obj.dorms.filter(id__in=assigned_dorms).exists():
                return True

        return False

    def has_change_permission(self, request, obj=None):
        """
        Only allow changes if the user is assigned to the dorm or is a ResLife Director.
        """
        if request.user.is_superuser:
            return True
        if obj is None:
            return True
        if hasattr(request.user, 'staffs'):
            staff_profile = request.user.staffs
            
            # Access the staff assignments (the reverse relation)
            staff_assignments = staff_profile.staffassignments.all()  # This will work now
            assigned_dorms = staff_assignments.values_list('dorm__id', flat=True)

            # Check if the staff is assigned to the dorm for the current object
            if obj.dorms.filter(id__in=assigned_dorms).exists():
                return True

        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is None:
            return True
        if hasattr(request.user, 'staffs'):
            staff_profile = request.user.staffs
            
            # Access the reverse relation using the updated related_name 'staffassignments'
            staff_assignments = staff_profile.staffassignments.all()  # Updated relation name
            
            # Get the assigned dorms for the staff
            assigned_dorms = staff_assignments.values_list('dorm__id', flat=True)

            # Check if the current object is assigned to the staff's dorms
            if obj.dorms.filter(id__in=assigned_dorms).exists():
                return True

        return False

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

class MaintenanceRequestResource(resources.ModelResource):
    dorm_name = fields.Field(
        attribute='dorm', column_name='Dorm Name',
        widget=ForeignKeyWidget(Dorm, 'name')
    )
    room_number = fields.Field(
        attribute='room', column_name='Room Number',
        widget=ForeignKeyWidget(Room, 'number')
    )
    resident_name = fields.Field(
        attribute='resident', column_name='Resident Name',
        widget=ForeignKeyWidget(Residents, 'user__email')
    )
    semester_name = fields.Field(
        attribute='semester', column_name='Semester',
        widget=ForeignKeyWidget(Semester, 'semester_type')
    )
    session_name = fields.Field(
        attribute='academic_session', column_name='Academic Session',
        widget=ForeignKeyWidget(AcademicSession, 'name')
    )
    category_name = fields.Field(
        attribute='category', column_name='Category',
        widget=ForeignKeyWidget(Category, 'name')
    )
    sub_category_name = fields.Field(
        attribute='sub_category', column_name='Subcategory',
        widget=ForeignKeyWidget(SubCategory, 'name')
    )
    updated_by_name = fields.Field(
        attribute='updated_by', column_name='Updated By',
        widget=ForeignKeyWidget(Staffs, 'user__email')
    )
    status_human_readable = fields.Field(
        column_name='Status',
        attribute='status'
    )
    
    def dehydrate_status_human_readable(self, obj):
        status_map = {
            MaintenanceRequest.PENDING: "Pending",
            MaintenanceRequest.IN_PROGRESS: "In Progress",
            MaintenanceRequest.COMPLETED: "Completed",
        }
        return status_map.get(obj.status, "Unknown")
    
    def dehydrate_created_date(self, obj):
        if obj.created_at:
            return DateFormat(obj.created_at).format('d/m/Y H:i')
        return ''

    def dehydrate_completion_date(self, obj):
        if obj.completion_date:
            return DateFormat(obj.completion_date).format('d/m/Y H:i')
        return ''

    class Meta:
        model = MaintenanceRequest
        fields = [
            'id', 'dorm_name', 'room_number', 'resident_name',
            'category_name', 'sub_category_name', 'description',
            'status_human_readable', 'created_at', 'completion_date',
            'updated_by_name', 'semester_name', 'session_name'
        ]
        export_order = [
            'id', 'dorm_name', 'room_number', 'resident_name',
            'semester_name', 'session_name', 'category_name', 'sub_category_name',
            'description', 'status_human_readable', 'created_at',
            'completion_date', 'updated_by_name'
        ]

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
    resource_class = MaintenanceRequestResource

    """
    1. A resident can view and create a MR-- they only need select and input 'category', 'sub_category', 'description'. the system captures 'id', 'resident', 'dorm', 'room', 'status', 'created_at', 'updated_at', 
        'completion_date', 'updated_by', 'semester', 'academic_session'

    2. same thing for Residence Assistance and Directors
    """

class SubCategoryAdmin(SortableAdminMixin,admin.ModelAdmin):
    list_display = ('name','my_order','category')
    search_fields = ('name','category')
    # model = SubCategory
    # extra = 1  # Number of empty subcategory forms to display
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
        is_reslife_director = self._is_reslife_directors(request)
        print(f"Checking view permission for ResLife Director: {is_reslife_director}")
        if request.user.is_superuser or is_reslife_director:
            return True
        return False
    # Overriding has_add_permission to allow adding for superusers and ResLife Directors
    def has_add_permission(self, request: HttpRequest, obj: SubCategory | None = None) -> bool:
        if request.user.is_superuser or self._is_reslife_directors(request):
            return True  # Superusers and ResLife Directors can add SubCategories
        return False  # All others are restricted from adding

    # Overriding has_change_permission to allow changing for superusers and ResLife Directors
    def has_change_permission(self, request: HttpRequest, obj: SubCategory | None = None) -> bool:
        if request.user.is_superuser or self._is_reslife_directors(request):
            return True  # Superusers and ResLife Directors can change SubCategories
        return False  # All others are restricted from changing

    # Overriding has_delete_permission to allow deleting for superusers and ResLife Directors
    def has_delete_permission(self, request: HttpRequest, obj: SubCategory | None = None) -> bool:
        if request.user.is_superuser or self._is_reslife_directors(request):
            return True  # Superusers and ResLife Directors can delete SubCategories
        return False

class CategoryAdmin(SortableAdminMixin,admin.ModelAdmin):
    # inlines = [SubCategoryInline]
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
admin.site.register(SubCategory, SubCategoryAdmin)



