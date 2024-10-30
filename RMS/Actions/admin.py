from django.core.exceptions import ValidationError
from django.contrib import admin
from .models import MaintenanceRequest, Category, SubCategory, Announcement, Complaint
from adminsortable2.admin import SortableAdminMixin
from .forms import ComplaintForm
from UserProfiles.models import Staffs
from AcademicYear.models import Enrollment
from django.http import HttpRequest

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

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'enrollment', 'semester', 'academic_session', 'is_anonymous')
    list_filter = ('semester', 'academic_session', 'is_anonymous')
    search_fields = ('user__username', 'description')
    # ordering = ('created_at',)
    form = ComplaintForm

    def _is_reslife_directors(self, request: HttpRequest) -> bool:
        """Checks if the user is a ResLife Director."""
        staff = Staffs.objects.filter(user=request.user).first()
        return staff and staff.role.name == 'ResLife Directors'

    def get_queryset(self, request: HttpRequest):
        """Restrict complaints based on user roles and access permissions."""
        queryset = super().get_queryset(request)
        
        # Check if the user is a superuser
        if request.user.is_superuser:
            return queryset  # Superusers can see all complaints

        # Check if the user has the 'Judicial Affairs' role
        if request.user.staffs.filter(role__name='Judicial Affairs').exists():
            return queryset  # Judicial Affairs can see all complaints, including anonymous

        # Allow Dean of Student Affairs to view all complaints
        if request.user.staffs.filter(role__name='Dean of Student Affairs').exists():
            return queryset  # Deans can see all complaints, including anonymous

        # Allow President to view all complaints
        if request.user.staffs.filter(role__name='President').exists():
            return queryset  # President can see all complaints, including anonymous

        # Allow ResLife Directors to view complaints for their assigned dorms
        staff = Staffs.objects.filter(user=request.user).first()
        if staff and staff.role.name in ['ResLife Director', 'Residence Assistant']:
            # Return complaints related to the dorms the staff is assigned to
            assigned_dorms = staff.staffassignment_set.values_list('dorm', flat=True)
            return queryset.filter(dorm__in=assigned_dorms)

        # For residents, allow viewing only their own complaints
        if hasattr(request.user, 'resident'):
            return queryset.filter(resident__user=request.user)  # Residents see their own complaints

        return queryset.none()  # No access for anyone else
    
    def has_view_permission(self, request: HttpRequest, obj: Complaint | None = None) -> bool:
        """Define view permissions."""
        if request.user.is_superuser:
            return True  # Superusers can view any complaint

        # Allow Dean of Student Affairs to view any complaints
        if request.user.staffs.filter(role__name='Dean of Student Affairs').exists():
            return True

        # Allow President to view any complaints
        if request.user.staffs.filter(role__name='President').exists():
            return True

        # Allow ResLife Directors to view complaints for their assigned dorms
        staff = Staffs.objects.filter(user=request.user).first()
        if staff and staff.role.name in ['ResLife Director', 'Residence Assistant']:
            if obj and obj.dorm in staff.staffassignment_set.values_list('dorm', flat=True):
                return True  # Assigned staff can view complaints in their dorm

        # Allow residents to view their own complaints
        if hasattr(request.user, 'resident'):
            return obj is None or (obj.resident.user == request.user)  # Residents see their own complaints

        return False  # No access otherwise

    def has_add_permission(self, request: HttpRequest) -> bool:
        """Define add permissions."""
        if request.user.is_superuser:
            return True  # Superusers can add complaints

        # Residents can add their own complaints
        if hasattr(request.user, 'resident'):
            return True  # Residents can add complaints for themselves

        # ResLife Directors and Residence Assistants can add complaints for their dorms
        staff = Staffs.objects.filter(user=request.user).first()
        if staff and staff.role.name in ['ResLife Director', 'Residence Assistant']:
            return True  # They can add complaints for their assigned dorms

        return False  # No other roles can add complaint
    
    def has_change_permission(self, request: HttpRequest, obj: Complaint | None = None) -> bool:
        """Allow only authorized staff to update complaints."""
        if request.user.is_superuser or self._is_dean_of_student_affairs(request) or self._is_reslife_director(request):
            return True  # Superuser, Deans, and ResLife Directors can update anything

    def has_delete_permission(self, request: HttpRequest, obj: Complaint | None = None) -> bool:
        """Allow only superusers and authorized staff to delete complaints."""
        if request.user.is_superuser:
            return True  # Superuser, Deans, and ResLife Directors can delete anything

@admin.register(MaintenanceRequest)
class MaintenanceRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'resident', 'dorm', 'room', 'category', 'sub_category','description', 'status', 'created_at', 'updated_at', 'completion_date', 'updated_by']
    list_filter = ['status', 'category', 'sub_category', 'created_at', 'updated_at', 'completion_date']
    search_fields = ['id', 'resident__user__username', 'dorm__name', 'room__room_number', 'category', 'sub_category']
    readonly_fields = ['created_at', 'updated_at', 'completion_date']

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
            if staff.role.name in ['ResLife Director', 'Dean of Student Affairs']:
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
            if staff.role.name == 'ResLife Director':
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
        if staff and staff.role.name in ['ResLife Director', 'Dean of Student Affairs']:
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
        if staff and staff.role.name in ['ResLife Director', 'Dean of Student Affairs']:
            return True  # ResLife Directors and Dean can update all requests

        # Check if the staff is assigned to the dorm
        if obj and self._is_staff_assigned_to_dorm(request, obj):
            if staff.role.name in ['Residence Assistant', 'Residence Director']:
                return True  # Assigned staff can delete requests in their dorm

        return False  # Deny access otherwise

class SubCategoryInline(SortableAdminMixin,admin.TabularInline):
    list_display = ('name','my_order')
    search_fields = ('name',)
    model = SubCategory
    extra = 1  # Number of empty subcategory forms to display
    ordering = ['my_order']

class CategoryAdmin(SortableAdminMixin,admin.ModelAdmin):
    inlines = [SubCategoryInline]
    list_display = ('name','my_order')
    search_fields = ('name',)
    ordering = ['my_order']


admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory)



