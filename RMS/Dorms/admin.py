from django.contrib import admin
from django.shortcuts import render, redirect
from .models import Dorm, Room,Storage,StorageItem
from .forms import RoomGenerationForm

@admin.register(Dorm)
class DormAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'gender', 'campus_status', 'room_count')
    search_fields = ('name', 'address')
    ordering = ('name',)
    actions = ['show_generate_rooms_form']

    def room_count(self, obj):
        return obj.rooms.count()
    room_count.short_description = 'Room Count'

    def show_generate_rooms_form(self, request, queryset):
        if 'apply' in request.POST:
            form = RoomGenerationForm(request.POST)
            if form.is_valid():
                dorm = form.cleaned_data['dorm']
                room_range = form.cleaned_data['range']
                self.generate_rooms(dorm, room_range)
                self.message_user(request, "Rooms generated successfully.")
                return redirect('admin:dorms_dorm_changelist')
        else:
            form = RoomGenerationForm()
        return render(request, 'admin/generate_rooms.html', {'form': form})

    def generate_rooms(self, dorm, room_range):
        start_num, end_num = map(int, room_range.split('-'))
        for num in range(start_num, end_num + 1):
            room_number = str(num).zfill(3)
            Room.objects.create(
                number=room_number,
                capacity=2,  # Adjust as needed
                room_plan='2_in_1_wof',  # Adjust as needed
                floor=1,  # Adjust as needed
                dorm=dorm
            )

    show_generate_rooms_form.short_description = "Generate Rooms"

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('id' ,'number','room_name', 'capacity', 'room_plan', 'floor', 'dorm')
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
