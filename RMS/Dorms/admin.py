from django.contrib import admin
from .models import Dorm, Room, Storage, StorageItem

@admin.register(Dorm)
class DormAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address', 'gender', 'campus_status','capacity')
    list_filter = ('gender', 'campus_status')
    search_fields = ('name', 'address')
    ordering = ('id',)

    def uuid(self, obj):
        return obj.uuid

    uuid.short_description = 'UUID'

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'uuid', 'number', 'capacity', 'floor', 'dorm')
    list_filter = ('dorm__name',)
    search_fields = ('number', 'dorm__name')
    ordering = ('id',)

    def uuid(self, obj):
        return obj.uuid

    uuid.short_description = 'UUID'

@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    list_display = ('id', 'uuid', 'description', 'capacity', 'current_capacity', 'dorm')
    list_filter = ('dorm__name',)
    search_fields = ('description', 'dorm__name')
    ordering = ('id',)

    def uuid(self, obj):
        return obj.uuid

    uuid.short_description = 'UUID'

@admin.register(StorageItem)
class StorageItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'uuid', 'description', 'quantity', 'storage', 'room')
    list_filter = ('storage__dorm__name',)
    search_fields = ('description', 'storage__dorm__name')
    ordering = ('id',)

    def uuid(self, obj):
        return obj.uuid

    uuid.short_description = 'UUID'
