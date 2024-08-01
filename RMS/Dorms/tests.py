from django.contrib import admin
from django.shortcuts import render, redirect
from .models import Dorm, Room
from .forms import RoomGenerationForm

class DormAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'gender', 'campus_status', 'get_room_count')
    list_filter = ('gender', 'campus_status')
    search_fields = ('name', 'address')
    ordering = ('id',)
    actions = ['show_generate_rooms_form']

    def show_generate_rooms_form(self, request, queryset):
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
                return redirect('admin:dorms_dorm_changelist')
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

admin.site.register(Dorm, DormAdmin)
