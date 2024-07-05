# In dorms/admin.py

from django.contrib import admin
from .models import Dorm, Room, Storage, StorageItem

@admin.register(Dorm)
class DormAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'gender', 'campus_status')
    list_filter = ('gender', 'campus_status')
    search_fields = ('name', 'address')

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('number', 'capacity', 'floor', 'dorm')
    list_filter = ('dorm__name',)
    search_fields = ('number', 'dorm__name')

@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    list_display = ('description', 'capacity', 'current_capacity', 'dorm')
    list_filter = ('dorm__name',)
    search_fields = ('description', 'dorm__name')

@admin.register(StorageItem)
class StorageItemAdmin(admin.ModelAdmin):
    list_display = ('description', 'quantity', 'storage', 'room')
    list_filter = ('storage__dorm__name',)
    search_fields = ('description', 'storage__dorm__name')
