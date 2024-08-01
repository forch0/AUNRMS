from django.contrib import admin
from .models import Dorm, Room, Storage, StorageItem
from django.db import transaction
from django.urls import path
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django import forms
from .utils import create_rooms
# Define a form to select room ranges
class RoomRangeForm(forms.Form):
    RANGE_CHOICES = [
        ('101-116', '101-116'),
        ('201-216', '201-216'),
        ('301-316', '301-316'),
        ('2x2a-2x2b', '2x2a-2x2b'),
        ('3x3a-3x3b', '3x3a-3x3b'),
    ]
    ranges = forms.MultipleChoiceField(choices=RANGE_CHOICES, widget=forms.CheckboxSelectMultiple)
    capacity = forms.IntegerField(min_value=1, required=False, initial=3)
    room_plan = forms.CharField(max_length=20, required=False, initial='3_in_1_wf')
    floor = forms.IntegerField(min_value=1, max_value=4, required=False, initial=2)

# def create_rooms_action(modeladmin, request, queryset):
#     form = RoomRangeForm(request.POST or None)
#     if request.method == 'POST' and form.is_valid():
#         selected_ranges = form.cleaned_data['ranges']
#         capacity = form.cleaned_data['capacity']
#         room_plan = form.cleaned_data['room_plan']
#         floor = form.cleaned_data['floor']
        
#         for dorm in queryset:
#             create_rooms(dorm, selected_ranges, capacity, room_plan, floor)
        
#         modeladmin.message_user(request, "Rooms created successfully.")
#         return None  # Prevents default behavior

#     context = {
#         'title': "Create Rooms",
#         'form': form,
#     }
#     return modeladmin.render_change_form(request, None, context, change=False)

# create_rooms_action.short_description = "Create rooms with specified ranges"

@admin.register(Dorm)
class DormAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address', 'gender', 'campus_status','get_room_count')
    list_filter = ('gender', 'campus_status')
    search_fields = ('name', 'address')
    ordering = ('id',)
    actions = ['redirect_to_create_rooms']

    def redirect_to_create_rooms(self, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        return HttpResponseRedirect(f'/admin/dorms/dorm/{selected[0]}/create_rooms/')

    redirect_to_create_rooms.short_description = "Create rooms with specified ranges"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<path:object_id>/create_rooms/',
                self.admin_site.admin_view(self.create_rooms_view),
                name='create-rooms',
            ),
        ]
        return custom_urls + urls

    def create_rooms_view(self, request, object_id):
        dorm = self.get_object(request, object_id)
        if not dorm:
            return redirect('admin:dorms_dorm_changelist')

        if request.method == 'POST':
            form = RoomRangeForm(request.POST)
            if form.is_valid():
                selected_ranges = form.cleaned_data['ranges']
                capacity = form.cleaned_data['capacity']
                room_plan = form.cleaned_data['room_plan']
                floor = form.cleaned_data['floor']

                create_rooms(dorm, selected_ranges, capacity, room_plan, floor)
                self.message_user(request, "Rooms created successfully.")
                return redirect('admin:dorms_dorm_changelist')
        else:
            form = RoomRangeForm()

        context = {
            'form': form,
            'dorm': dorm,
            'opts': self.model._meta,
            'add': False,
            'change': False,
            'is_popup': False,
            'save_as': False,
            'has_view_permission': self.has_view_permission(request),
            'has_change_permission': self.has_change_permission(request, dorm),
            'has_add_permission': self.has_add_permission(request),
            'has_delete_permission': self.has_delete_permission(request, dorm),
        }
        return render(request, 'admin/create_rooms_form.html', context)

    def get_room_count(self, obj):
        return obj.rooms.count()
    get_room_count.short_description = 'Room Count'

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