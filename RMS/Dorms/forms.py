# forms.py
from django import forms
from .models import Dorm, Room

class RoomGenerationForm(forms.Form):
    dorm = forms.ModelChoiceField(queryset=Dorm.objects.all(), label="Dorm")
    range = forms.ChoiceField(choices=Room.RANGE_CHOICES, label="Predefined Range", required=False)
    range_start = forms.IntegerField(label="Start Number", required=False)
    range_end = forms.IntegerField(label="End Number", required=False)
    capacity = forms.IntegerField(label="Capacity", initial=3)
    room_plan = forms.ChoiceField(choices=Room.ROOM_OPTIONS, initial='3_in_1_wf')  # Default room plan
    floor = forms.ChoiceField(choices=Room.FLOOR_CHOICES, initial='ground')  # Default floor

    def clean(self):
        cleaned_data = super().clean()
        predefined_range = cleaned_data.get("range")
        range_start = cleaned_data.get("range_start")
        range_end = cleaned_data.get("range_end")

        if predefined_range and (range_start or range_end):
            raise forms.ValidationError("You can either select a predefined range or specify a custom range, not both.")

        if not predefined_range and (not range_start or not range_end):
            raise forms.ValidationError("Please provide a custom range with both start and end numbers.")

        return cleaned_data
