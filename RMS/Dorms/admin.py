from django.contrib import admin
from django.shortcuts import render, redirect
from .models import Dorm, Room, Storage, StorageItem
from .forms import RoomGenerationForm
from django.urls import reverse

class RoomGenerationAdmin(admin.ModelAdmin):
    form = RoomGenerationForm
    change_list_template = "admin/generate_rooms.html"

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('generate-rooms/', self.admin_site.admin_view(self.generate_rooms_view), name='generate-rooms'),
        ]
        return custom_urls + urls

    def generate_rooms_view(self, request):
        if request.method == 'POST':
            form = RoomGenerationForm(request.POST)
            if form.is_valid():
                dorm = form.cleaned_data['dorm']
                predefined_range = form.cleaned_data['range']
                range_start = form.cleaned_data['range_start']
                range_end = form.cleaned_data['range_end']
                capacity = form.cleaned_data['capacity']
                room_plan = form.cleaned_data['room_plan']
                floor = form.cleaned_data['floor']

                if predefined_range:
                    start, end = map(int, predefined_range.split('-'))
                    for number in range(start, end + 1):
                        Room.objects.create(
                            number=str(number),
                            capacity=capacity,
                            room_plan=room_plan,
                            floor=floor,
                            dorm=dorm
                        )
                else:
                    for number in range(range_start, range_end + 1):
                        Room.objects.create(
                            number=str(number),
                            capacity=capacity,
                            room_plan=room_plan,
                            floor=floor,
                            dorm=dorm
                        )
                self.message_user(request, "Rooms successfully created.")
                return redirect(reverse('admin:dorms_room_changelist'))

        else:
            form = RoomGenerationForm()
        return render(request, 'admin/generate_rooms.html', {'form': form})


@admin.register(Dorm)
class DormAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address', 'gender', 'campus_status', 'get_room_count')
    list_filter = ('gender', 'campus_status')
    search_fields = ('name', 'address')
    ordering = ('id',)
    actions = ['show_generate_rooms_form']

    def show_generate_rooms_form(self, request, queryset):
        return redirect('admin:generate-rooms')

    show_generate_rooms_form.short_description = "Generate Rooms"

    def get_room_count(self, obj):
        return obj.rooms.count()
    get_room_count.short_description = 'Room Count'

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'room_name', 'capacity', 'room_plan', 'floor', 'dorm')
    list_filter = ('dorm__name', 'room_plan', 'floor')
    search_fields = ('number', 'dorm__name')
    ordering = ('id',)

    def room_name(self, obj):
        return obj.number  # or adjust based on your needs
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
        'id', 'description', 'quantity', 'storage', 'room', 'resident', 'semester', 
        'academic_session', 'status', 'approved_by', 'approval_date', 'collected_at', 'collected_by'
    )
    list_filter = ('storage__dorm__name', 'status', 'approved_by')
    search_fields = ('description', 'storage__dorm__name', 'resident__name')
    ordering = ('id',)

    def collected_by(self, obj):
        return obj.collected_by.name if obj.collected_by else 'Not Collected'
    collected_by.short_description = 'Collected By'
