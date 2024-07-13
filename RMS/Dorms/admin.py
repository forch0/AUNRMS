from django.contrib import admin
from .models import Dorm, Room, Storage, StorageItem

@admin.register(Dorm)
class DormAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address', 'gender', 'campus_status', 'capacity')
    list_filter = ('gender', 'campus_status')
    search_fields = ('name', 'address')
    ordering = ('id',)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'capacity', 'room_plan', 'floor', 'dorm')
    list_filter = ('dorm', 'floor', 'room_plan')
    search_fields = ('number', 'dorm__name')
    ordering = ('id',)

@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'capacity', 'current_capacity', 'dorm')
    list_filter = ('dorm',)
    search_fields = ('description', 'dorm__name')
    ordering = ('id',)

@admin.register(StorageItem)
class StorageItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'quantity', 'storage', 'room')
    list_filter = ('storage__dorm',)
    search_fields = ('description', 'storage__dorm__name')
    ordering = ('id',)
