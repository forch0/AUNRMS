from django.contrib import admin
from .models import Dorm, Room, Storage, StorageItem
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import path
from django import forms

class GenerateRoomsForm(forms.Form):
    RANGE_CHOICES = [
        ('101-116', '101-116'),
        ('201-216', '201-216'),
        ('301-316', '301-316'),
        ('2x2a-2x2b', '2x2a-2x2b'),
        ('3x3a-3x3b', '3x3a-3x3b'),
    ]
    ranges = forms.MultipleChoiceField(
        choices=RANGE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

class DormAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'address', 'gender', 'campus_status', 'get_room_count']
    list_filter = ('gender', 'campus_status')
    search_fields = ('name', 'address',)
    ordering = ('id',)
    actions = ['show_generate_rooms_form']

    def get_room_count(self, obj):
        return obj.room_count()
    get_room_count.short_description = 'Room Count'

    def show_generate_rooms_form(self, request, queryset):
        if 'apply' in request.POST:
            form = GenerateRoomsForm(request.POST)
            if form.is_valid():
                selected_ranges = form.cleaned_data.get('ranges', [])
                if not selected_ranges:
                    self.message_user(request, "No ranges selected.")
                    return redirect(request.get_full_path())

                for dorm in queryset:
                    for range_choice in selected_ranges:
                        start, end = range_choice.split('-')
                        start_number = int(start)
                        end_number = int(end)

                        for number in range(start_number, end_number + 1):
                            room_number = f"{number:03d}"  # Format number with leading zeros
                            Room.objects.create(
                                number=room_number,
                                capacity=3,  # Adjust as needed
                                room_plan='3_in_1_wf',  # Adjust as needed
                                floor=1,  # Adjust as needed
                                dorm=dorm,
                                range=range_choice
                            )
                self.message_user(request, "Rooms have been generated for the selected dorms.")
                return redirect(request.get_full_path())
        else:
            form = GenerateRoomsForm()

        context = {
            'form': form,
            'title': 'Generate Rooms',
            'opts': self.model._meta,
        }
        return render(request, 'admin/generate_rooms_form.html', context)

    show_generate_rooms_form.short_description = "Generate Rooms for Selected Dorms"

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
