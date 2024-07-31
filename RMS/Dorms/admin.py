from django.contrib import admin
from .models import Dorm, Room, Storage, StorageItem

@admin.register(Dorm)
class DormAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address', 'gender', 'campus_status')
    list_filter = ('gender', 'campus_status')
    search_fields = ('name', 'address')
    ordering = ('id',)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'capacity', 'room_plan', 'floor', 'dorm')
    list_filter = ('dorm__name', 'room_plan', 'floor')
    search_fields = ('number', 'dorm__name')
    ordering = ('id',)

    def room_name(self, obj):
        return obj.room_name
    room_name.short_description = 'Room Name'

@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'capacity', 'current_capacity', 'floor', 'dorm')
    list_filter = ('dorm__name', 'floor')
    search_fields = ('description', 'dorm__name')
    ordering = ('id',)

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
        'collected_at', 
        'collected_by'
    )
    list_filter = ('storage__dorm__name', 'status', 'approved_by')
    search_fields = ('description', 'storage__dorm__name', 'resident__name')
    ordering = ('id',)

    def collected_by(self, obj):
        return obj.collected_by.name if obj.collected_by else 'Not Collected'
    collected_by.short_description = 'Collected By'