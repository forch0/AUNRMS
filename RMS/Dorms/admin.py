from django.contrib import admin
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Dorm, Room, Storage, StorageItem
from .forms import RoomGenerationForm

@admin.register(Dorm)
class DormAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'gender', 'campus_status', 'get_room_count')
    list_filter = ('gender', 'campus_status')
    search_fields = ('name', 'address')
    ordering = ('id',)
    actions = ['generate_rooms']

    def generate_rooms(self, request, queryset):
        if 'apply' in request.POST:
            form = RoomGenerationForm(request.POST)
            if form.is_valid():
                dorm = form.cleaned_data.get('dorm')
                range_choice = form.cleaned_data.get('range')
                range_start = form.cleaned_data.get('range_start')
                range_end = form.cleaned_data.get('range_end')
                capacity = form.cleaned_data.get('capacity')
                room_plan = form.cleaned_data.get('room_plan')
                floor = form.cleaned_data.get('floor')

                if range_choice:
                    self.create_rooms_from_choice(dorm, range_choice, capacity, room_plan, floor)
                elif range_start and range_end:
                    self.create_rooms_from_manual(dorm, range_start, range_end, capacity, room_plan, floor)

                self.message_user(request, "Rooms have been generated.")
                return redirect(reverse('admin:dorms_dorm_changelist'))
        else:
            form = RoomGenerationForm()

        context = {
            'form': form,
            'title': "Generate Rooms",
        }
        return render(request, 'admin/generate_rooms.html', context)

    def create_rooms_from_choice(self, dorm, range_choice, capacity, room_plan, floor):
        ranges = {
            '101-116': (101, 116),
            '201-216': (201, 216),
            '301-316': (301, 316),
            # Add more predefined ranges here if needed
        }
        start, end = ranges.get(range_choice, (0, 0))
        for number in range(start, end + 1):
            Room.objects.create(
                number=number,
                capacity=capacity,
                room_plan=room_plan,
                floor=floor,
                dorm=dorm,
            )

    def create_rooms_from_manual(self, dorm, start, end, capacity, room_plan, floor):
        for number in range(start, end + 1):
            Room.objects.create(
                number=number,
                capacity=capacity,
                room_plan=room_plan,
                floor=floor,
                dorm=dorm,
            )

    def get_room_count(self, obj):
        return obj.rooms.count()
    get_room_count.short_description = 'Number of Rooms'
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'room_name', 'capacity', 'room_plan', 'floor', 'dorm')
    list_filter = ('dorm__name', 'room_plan', 'floor')
    search_fields = ('number', 'dorm__name')
    ordering = ('id',)

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
