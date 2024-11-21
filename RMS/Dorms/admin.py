from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Dorm, Room, Storage, StorageItem
from .forms import RoomGenerationForm, StorageItemForm
from AcademicYear.models import Semester,Enrollment,StaffAssignment
from typing import Any
from django.http import HttpRequest
from UserProfiles.models import Staffs,Residents

@admin.register(Dorm)
class DormAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'gender', 'campus_status', 'room_count','occupancy_ratio', 'is_full')
    list_filter = ('gender', 'campus_status')
    search_fields = ('name', 'address')
    ordering = ('name',)
    
    def room_count(self, obj):
        """Returns the count of rooms in the dorm."""
        return obj.room_count()

    def occupancy_ratio(self, obj):
        """Returns the occupancy ratio of the dorm."""
        semester = Semester.objects.latest('start_date')  # Get the most recent semester
        return obj.occupancy_ratio(semester)

    def is_full(self, obj):
        """Returns if the dorm is full."""
        semester = Semester.objects.latest('start_date')  # Get the most recent semester
        return obj.is_full(semester)
    # Permission Helper Methods
    def _is_superuser(self, request: HttpRequest) -> bool:
        """Checks if the user is a Django superuser."""
        return request.user.is_superuser

    def _has_selected_roles(self, request: HttpRequest) -> bool:
        """Checks if the user has one of the allowed roles."""
        allowed_roles = ['ResLife Directors','Resid']  # Add the role names you want here
        staff = Staffs.objects.filter(user=request.user).first()
        if staff:
            return staff.role.name in allowed_roles
        return False
    # # Permissions
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

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'room_name', 'capacity', 'room_plan', 'floor', 'dorm', 'occupancy_ratio','is_full')
    list_filter = ('dorm__name', 'room_plan', 'floor')
    search_fields = ('number', 'dorm__name')
    ordering = ('id',)

    @admin.display(description='Occupancy Ratio')
    def occupancy_ratio(self, obj):
        """Returns the occupancy ratio in the format '1/3'."""
        return obj.occupancy_ratio()

    
    # is_occupied.boolean = True  # Display as a boolean icon in admin
    # is_full.boolean = True  # Display as a boolean icon in admin
    # Helper Methods for Permissions
    def _is_superuser(self, request: HttpRequest) -> bool:
        """Checks if the user is a Django superuser."""
        return request.user.is_superuser

    def _has_selected_roles(self, request: HttpRequest) -> bool:
        """Checks if the user has one of the allowed roles."""
        allowed_roles = ['ResLife Directors']  # Add other allowed role names as needed
        staff = Staffs.objects.filter(user=request.user).first()
        return staff and staff.role.name in allowed_roles

    def _is_resident(self, request: HttpRequest) -> bool:
        """Checks if the user is a resident."""
        return hasattr(request.user, 'residents')

    def _resident_room(self, request: HttpRequest):
        """Gets the room assigned to the resident for the current semester."""
        current_semester = Semester.objects.latest('start_date')
        resident = Residents.objects.filter(user=request.user).first()
        if resident:
            enrollment = Enrollment.objects.filter(resident=resident, semester=current_semester).first()
            if enrollment:
                return enrollment.room
        return None

    def _assigned_dorms(self, request: HttpRequest):
        """Gets the dorms assigned to the Residence Director and Residence Assistant for the current semester."""
        current_semester = Semester.objects.latest('start_date')
        staff = Staffs.objects.filter(user=request.user).first()
        
        # Check if the user is a Residence Director or Residence Assistant
        if staff and staff.role.name in ['Residence Director', 'Residence Assistant']:
            assignments = StaffAssignment.objects.filter(staff=staff, semester=current_semester)
            return [assignment.dorm for assignment in assignments]
        return []
    
    # Permissions
    def has_view_permission(self, request: HttpRequest, obj: Any | None = None) -> bool:
        """
        Allows:
        - Superusers to view all rooms.
        - All ResLife Directors to view all rooms.
        - Residence Assistants to view rooms assigned to them for the current semester.
        - Residents to view only their assigned room.
        """
        if self._is_superuser(request):
            return True

        # Check if the user is a ResLife Director
        if self._has_selected_roles(request):
            return True  # Allow all ResLife Directors to view all rooms

        # Check if the user is a resident
        if self._is_resident(request):
            resident_room = self._resident_room(request)
            # Allow resident to view only their assigned room
            return obj is None or obj == resident_room

        return False  # Deny access for other users

    def has_add_permission(self, request: HttpRequest) -> bool:
        """Only superuser and ResLife Directors can add rooms."""
        return self._is_superuser(request) or self._has_selected_roles(request)

    def has_change_permission(self, request: HttpRequest, obj: Any | None = None) -> bool:
        """Only superuser and ResLife Directors can change rooms."""
        return self._is_superuser(request) or self._has_selected_roles(request)

    def has_delete_permission(self, request: HttpRequest, obj: Any | None = None) -> bool:
        """Only superuser and ResLife Directors can delete rooms."""
        return self._is_superuser(request) or self._has_selected_roles(request)

@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'capacity', 'current_capacity', 'floor', 'dorm')
    list_filter = ('dorm__name', 'floor')
    search_fields = ('description', 'dorm__name')
    ordering = ('id',)

    # Helper method to check if user is a superuser
    def _is_superuser(self, request: HttpRequest) -> bool:
        return request.user.is_superuser

    # Helper method to check if the user has the 'ResLife Director' role
    def _has_reslife_director_role(self, request: HttpRequest) -> bool:
        staff = Staffs.objects.filter(user=request.user).first()
        return staff and staff.role.name == 'ResLife Directors'

    # Helper method to check if the user has the 'Residence Director' role
    def _has_residence_director_role(self, request: HttpRequest) -> bool:
        staff = Staffs.objects.filter(user=request.user).first()
        return staff and staff.role.name == 'Residence Director'

    # Check if user has permission to view storage
    def has_view_permission(self, request: HttpRequest, obj=None) -> bool:
        return self._is_superuser(request) or self._has_reslife_director_role(request) or self._has_residence_director_role(request)

    # Check if user has permission to add a storage item
    def has_add_permission(self, request: HttpRequest) -> bool:
        return self._is_superuser(request) or self._has_reslife_director_role(request) or self._has_residence_director_role(request)

    # Check if user has permission to change a storage item
    def has_change_permission(self, request: HttpRequest, obj=None) -> bool:
        return self._is_superuser(request) or self._has_reslife_director_role(request) or self._has_residence_director_role(request)

    # Check if user has permission to delete a storage item
    def has_delete_permission(self, request: HttpRequest, obj=None) -> bool:
        return self._is_superuser(request) or self._has_reslife_director_role(request) or self._has_residence_director_role(request)



@admin.register(StorageItem)
class StorageItemAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'description', 
        'quantity', 
        'storage', 
        'room', 
        'resident', 
        'semester', 
        'academic_session', 
        'status', 
        'approved_by', 
        'approval_date', 
        'item_type',
        # 'display_collected_at', 
        # 'display_collected_by'
    )
    list_filter = ('status', 'approved_by')
    search_fields = ('description', 'storage__dorm__name', 'resident__name')
    ordering = ('id',)
    autocomplete_fields = ['storage','resident','room','semester','academic_session','approved_by','collected_by',  ]
    readonly_fields = ('approval_date', 'created_at')
    actions = ['mark_as_collected']

    # if request.user.is_superuser or self._has_selected_roles(request, allowed_roles=['ResLife Directors']):
    # 'Residence Director'

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if request.user.is_superuser:
            return qs  # Superusers see all items

        # Get staff member for checking role
        staff_member = request.user.staffs  # Access the related Staffs object

        if staff_member:
            # ResLife Directors have full access, just like Superusers
            if staff_member.role.name == 'ResLife Director':
                return qs  # ResLife Directors see all items for their dorm

            # Residence Assistants see only items assigned to them for their dorm
            if staff_member.role.name in ['Residence Assistant', 'Residence Director']:
                recent_assignment = StaffAssignment.objects.filter(staff=staff_member).order_by('-created_at').first()
                if recent_assignment:
                    return qs.filter(storage__room__dorm=recent_assignment.dorm, collected_by__isnull=True)

    # If the user is a resident, show only items assigned to them or their own items
        logged_in_resident = Residents.objects.filter(user=request.user).first()
        if logged_in_resident:
            return qs.filter(collected_by=logged_in_resident)  # Items assigned to the logged-in resident

        return qs.none()  # If no applicable items, show nothing

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser or (request.user.is_staff and request.user.staffs.role.name == 'ResLife Directors'):
            return True  # Superusers and ResLife Directors can view all items

        staff_member = request.user.staffs  # Access the related Staffs object
        if staff_member:
            if staff_member.role.name in ['Residence Assistant', 'Residence Director']:
                return True  # Residence Assistants and Residence Directors can view items for their assigned dorm

        logged_in_resident = Residents.objects.filter(user=request.user).first()
        if logged_in_resident:
            return True  # Residents can view their own items

        return False

    def has_add_permission(self, request):
        if request.user.is_superuser or (request.user.is_staff and request.user.staffs.role.name == 'ResLife Directors'):
            return True  # Superusers and ResLife Directors can add items

        staff_member = request.user.staffs  # Access the related Staffs object
        if staff_member:
            if staff_member.role.name in ['Residence Assistant', 'Residence Director']:
                return True  # Residence Assistants and Residence Directors can add items in their assigned dorm

        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser or (request.user.is_staff and request.user.staffs.role.name == 'ResLife Directors'):
            return True  # Superusers and ResLife Directors can change items

        staff_member = request.user.staffs  # Access the related Staffs object
        if staff_member:
            if staff_member.role.name in ['Residence Assistant', 'Residence Director']:
                return True  # Residence Assistants and Residence Directors can change items in their assigned dorm

        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser or (request.user.is_staff and request.user.staffs.role.name == 'ResLife Directors'):
            return True  # Superusers and ResLife Directors can delete items

        staff_member = request.user.staffs  # Access the related Staffs object
        if staff_member:
            if staff_member.role.name in ['Residence Assistant', 'Residence Director']:
                return True  # Residence Assistants and Residence Directors can delete items in their assigned dorm

        return False

    def item_type(self, obj):
        logged_in_resident = Residents.objects.filter(user=self.request.user).first()
        if logged_in_resident:
            if obj.resident == logged_in_resident:
                return format_html('<strong>My Item</strong>')  # Display "My Item" if the item belongs to the logged-in resident
            else:
                return format_html('<span style="color: red;">Assigned to Collect</span>')  # Display differently if it's assigned to collect
        return "Unknown"
    item_type.short_description = "Item Type"

    def mark_as_collected(self, request, queryset):
        """Action to mark selected items as collected"""
        for item in queryset:
            item.status = StorageItem.APPROVED
            item.collected_at = timezone.now()  # Add collection timestamp
            item.save()
        self.message_user(request, f"{queryset.count()} items marked as collected.")
    mark_as_collected.short_description = "Mark selected items as collected"