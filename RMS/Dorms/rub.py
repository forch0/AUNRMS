def show_generate_rooms_form(self, request, queryset):
        if 'apply' in request.POST:
            form = RoomGenerationForm(request.POST)
            if form.is_valid():
                dorm = form.cleaned_data.get('dorm')
                range_choice = form.cleaned_data.get('range_choice')
                range_start = form.cleaned_data.get('range_start')
                range_end = form.cleaned_data.get('range_end')
                capacity = form.cleaned_data.get('capacity')
                room_plan = form.cleaned_data.get('room_plan')
                floor = form.cleaned_data.get('floor')

                if range_choice:
                    self.create_rooms_from_choice(dorm, range_choice, capacity, room_plan, floor)
                elif range_start is not None and range_end is not None:
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
        room_numbers = [int(num) for num in range_choice.split(',') if num.strip().isdigit()]
        for room_number in room_numbers:
            Room.objects.create(
                dorm=dorm,
                number=room_number,
                capacity=capacity,
                room_plan=room_plan,
                floor=floor
            )

def create_rooms_from_manual(self, dorm, range_start, range_end, capacity, room_plan, floor):

        for room_number in range(range_start, range_end + 1):
            Room.objects.create(
                dorm=dorm,
                number=room_number,
                capacity=capacity,
                room_plan=room_plan,
                floor=floor
            )


        for room_number in range(range_start, range_end + 1):
            Room.objects.create(
                dorm=dorm,
                number=room_number,
                capacity=capacity,
                room_plan=room_plan,
                floor=floor
            )


# def generate_rooms(request):
#     if request.method == 'POST':
#         form = RoomGenerationForm(request.POST)
#         if form.is_valid():
#             dorm = form.cleaned_data.get('dorm')
#             range_choice = form.cleaned_data.get('range')
#             range_start = form.cleaned_data.get('range_start')
#             range_end = form.cleaned_data.get('range_end')
#             capacity = form.cleaned_data.get('capacity')
#             room_plan = form.cleaned_data.get('room_plan')
#             floor = form.cleaned_data.get('floor')

#             if range_choice:
#                 create_rooms_from_choice(dorm, range_choice, capacity, room_plan, floor)
#             elif range_start and range_end:
#                 create_rooms_from_manual(dorm, range_start, range_end, capacity, room_plan, floor)

#             # Redirect to the Django admin home page
#             return redirect(reverse('admin:index'))

#     else:
#         form = RoomGenerationForm()

#     context = {
#         'form': form,
#         'title': "Generate Rooms",
#     }
#     return render(request, 'admin/generate_rooms.html', context)

# def create_rooms_from_choice(dorm, range_choice, capacity, room_plan, floor):
#     ranges = {
#         '101-116': (101, 116),
#         '201-216': (201, 216),
#         '301-316': (301, 316),
#         # Add more predefined ranges here if needed
#     }
#     start, end = ranges.get(range_choice, (0, 0))
#     for number in range(start, end + 1):
#         Room.objects.create(
#             number=number,
#             capacity=capacity,
#             room_plan=room_plan,
#             floor=floor,
#             dorm=dorm,
#         )

# def create_rooms_from_manual(dorm, start, end, capacity, room_plan, floor):
#     for number in range(start, end + 1):
#         Room.objects.create(
#             number=number,
#             capacity=capacity,
#             room_plan=room_plan,
#             floor=floor,
#             dorm=dorm,
#         )

