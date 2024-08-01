# views.py
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import RoomGenerationForm
from .models import Dorm, Room
from django.http import HttpResponse

def index(request):
    return HttpResponse("Welcome to Dorms Section.")
    pass

def generate_rooms(request):
    if request.method == 'POST':
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
                create_rooms_from_choice(dorm, range_choice, capacity, room_plan, floor)
            elif range_start and range_end:
                create_rooms_from_manual(dorm, range_start, range_end, capacity, room_plan, floor)

            # Use the correct admin URL namespace for the changelist view
            # return redirect(reverse('admin:dorms_dorm_changelist'))
            # Redirect to the Django admin home page
            return redirect(reverse('admin:index'))
            
        

    else:
        form = RoomGenerationForm()

    context = {
        'form': form,
        'title': "Generate Rooms",
    }
    return render(request, 'admin/generate_rooms.html', context)

def create_rooms_from_choice(dorm, range_choice, capacity, room_plan, floor):
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

def create_rooms_from_manual(dorm, start, end, capacity, room_plan, floor):
    for number in range(start, end + 1):
        Room.objects.create(
            number=number,
            capacity=capacity,
            room_plan=room_plan,
            floor=floor,
            dorm=dorm,
        )

