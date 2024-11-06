from django.contrib import admin
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
    list_display = ('name', 'address', 'gender', 'campus_status', 'get_room_count','total_capacity','occupancy_ratio_display', 'is_full_display')
    list_filter = ('gender', 'campus_status')
    search_fields = ('name', 'address')
    ordering = ('name',)
    
    
    def get_room_count(self, obj):
        return obj.room_count()
    get_room_count.short_description = 'Room Count'

    def total_capacity(self, obj):
        return obj.total_capacity()
    total_capacity.short_description = 'Total Capacity'

    def occupancy_ratio_display(self, obj):
        # You may need to pass a specific semester here if necessary
        current_semester = Semester.objects.latest('start_date')  # Example: latest semester
        return obj.occupancy_ratio(current_semester)
    occupancy_ratio_display.short_description = 'Occupancy Ratio'

    def is_full_display(self, obj):
        current_semester = Semester.objects.latest('start_date')  # Example: latest semester
        return 'Yes' if obj.is_full(current_semester) else 'No'
    is_full_display.short_description = 'Is Full'

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
    list_display = ('id', 'number', 'room_name', 'capacity', 'room_plan', 'floor', 'dorm', 'is_occupied')
    list_filter = ('dorm__name', 'room_plan', 'floor')
    search_fields = ('number', 'dorm__name')
    ordering = ('id',)

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

@admin.register(StorageItem)
class StorageItemAdmin(admin.ModelAdmin):
    form = StorageItemForm
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
        'collected_at', 
        'collected_by'
    )
    list_filter = ('storage__dorm__name', 'status', 'approved_by')
    search_fields = ('description', 'storage__dorm__name', 'resident__name')
    ordering = ('id',)
    autocomplete_fields = ['room']

    def collected_by(self, obj):
        return obj.collected_by.name if obj.collected_by else 'Not Collected'
    collected_by.short_description = 'Collected By'

    # Helper Methods for Permissions
    def _is_superuser(self, request: HttpRequest) -> bool:
        """Checks if the user is a superuser."""
        return request.user.is_superuser

    def _has_selected_roles(self, request: HttpRequest, allowed_roles=['ResLife Director']) -> bool:
        """Checks if the user has one of the allowed roles."""
        staff = Staffs.objects.filter(user=request.user).first()
        return staff and staff.role.name in allowed_roles

    def _is_resident(self, request: HttpRequest) -> bool:
        """Checks if the user is a resident."""
        return hasattr(request.user, 'residents')

    def _resident_storage_items(self, request: HttpRequest):
        """Filters storage items to those belonging to the logged-in resident."""
        resident = Residents.objects.filter(user=request.user).first()
        if resident:
            return StorageItem.objects.filter(resident=resident)
        return StorageItem.objects.none()

    # Permissions
    def has_view_permission(self, request: HttpRequest, obj: Any | None = None) -> bool:
        """Allows superuser, ResLife Director, and residents to view relevant storage items."""
        if self._is_superuser(request) or self._has_selected_roles(request):
            return True
        if self._is_resident(request):
            return obj is None or obj.resident.user == request.user
        return False  # All other users are denied access.

    def has_add_permission(self, request: HttpRequest) -> bool:
        """Only superuser and ResLife Directors can add storage items."""
        return self._is_superuser(request) or self._has_selected_roles(request)

    def has_change_permission(self, request: HttpRequest, obj: Any | None = None) -> bool:
        """Only superuser and ResLife Directors can change storage items."""
        return self._is_superuser(request) or self._has_selected_roles(request)

    def has_delete_permission(self, request: HttpRequest, obj: Any | None = None) -> bool:
        """Only superuser and ResLife Directors can delete storage items."""
        return self._is_superuser(request) or self._has_selected_roles(request)

    def get_queryset(self, request: HttpRequest):
        """Filters the queryset based on the user’s role."""
        qs = super().get_queryset(request)

        if self._is_superuser(request) or self._has_selected_roles(request):
            return qs  # Full access for superusers and ResLife Directors

        if self._is_resident(request):
            return self._resident_storage_items(request)  # Only resident’s storage items

        return qs.none()  # Deny access to all other users

    # def has_module_permission(self, request: HttpRequest) -> bool:
        """Allows access to the StorageItem admin based on roles."""
        return (
            self._is_superuser(request) 
            or self._has_selected_roles(request) 
            or self._is_resident(request)
        )