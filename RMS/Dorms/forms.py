from django import forms
from .models import Dorm,Room

class RoomGenerationForm(forms.Form):
    dorm = forms.ModelChoiceField(queryset=Dorm.objects.all(), label="Dorm")
    range = forms.ChoiceField(choices=Room.RANGE_CHOICES, label="Predefined Range", required=False)
    range_start = forms.IntegerField(label="Start Number", required=False)
    range_end = forms.IntegerField(label="End Number", required=False)
    capacity = forms.IntegerField(label="Capacity", initial=3)
    room_plan = forms.ChoiceField(choices=Room.ROOM_OPTIONS, initial='3_in_1_wf')  # Default room plan
    floor = forms.ChoiceField(choices=Room.FLOOR_CHOICES, initial='ground')
    def clean(self):
        cleaned_data = super().clean()
        range_choice = cleaned_data.get('range_choice')
        range_start = cleaned_data.get('range_start')
        range_end = cleaned_data.get('range_end')

        if not (range_choice or (range_start is not None and range_end is not None)):
            raise forms.ValidationError("You must provide a range choice or a start and end range.")
        if range_start is not None and range_end is not None and range_start > range_end:
            raise forms.ValidationError("Start range must be less than or equal to end range.")
        

