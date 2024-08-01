# from .models import Dorm, Room
# import uuid

# def create_rooms(dorm, ranges, capacity=3, room_plan='3_in_1_wf', floor=2):
#     """
#     Create rooms in the specified ranges for a given dorm.
#     :param dorm: The dorm to add rooms to.
#     :param ranges: A list of ranges and patterns to create rooms.
#     :param capacity: The capacity for the new rooms.
#     :param room_plan: The room plan for the new rooms.
#     :param floor: The floor for the new rooms.
#     """
#     existing_room_numbers = Room.objects.filter(dorm=dorm).values_list('number', flat=True)
    
#     for range_str in ranges:
#         if '-' in range_str:  # Numeric range
#             start, end = map(int, range_str.split('-'))
#             for number in range(start, end + 1):
#                 room_number = str(number)
#                 if room_number not in existing_room_numbers:
#                     Room.objects.create(
#                         id=uuid.uuid4(),  # Ensures unique UUID
#                         number=room_number,
#                         capacity=capacity,
#                         room_plan=room_plan,
#                         floor=floor,
#                         dorm=dorm
#                     )
#         elif 'x' in range_str:  # Pattern range
#             base, suffixes = range_str.split('x')
#             for suffix in suffixes.split('-'):
#                 room_number = f"{base}x{suffix}"
#                 if room_number not in existing_room_numbers:
#                     Room.objects.create(
#                         id=uuid.uuid4(),  # Ensures unique UUID
#                         number=room_number,
#                         capacity=capacity,
#                         room_plan=room_plan,
#                         floor=floor,
#                         dorm=dorm
#                     )

# utils.py
import uuid
from .models import Room

def create_rooms(dorm, ranges, capacity, room_plan, floor):
    for room_range in ranges:
        if '-' in room_range:
            start, end = room_range.split('-')
            start_num = int(start)
            end_num = int(end)
            for number in range(start_num, end_num + 1):
                Room.objects.get_or_create(
                    number=str(number),
                    dorm=dorm,
                    defaults={
                        'capacity': capacity,
                        'room_plan': room_plan,
                        'floor': floor,
                        'id': uuid.uuid4()
                    }
                )
        else:
            start, end = room_range.split('x')
            start_num = int(start)
            end_num = int(end)
            for number in range(start_num, end_num + 1):
                Room.objects.get_or_create(
                    number=f'{number}x',
                    dorm=dorm,
                    defaults={
                        'capacity': capacity,
                        'room_plan': room_plan,
                        'floor': floor,
                        'id': uuid.uuid4()
                    }
                )
