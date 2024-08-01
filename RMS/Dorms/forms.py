from django import forms
from .models import Dorm,Room

class RoomGenerationForm(forms.Form):
    dorm = forms.ModelChoiceField(queryset=Dorm.objects.all(), label="Dorm")
    range = forms.ChoiceField(choices=Room.RANGE_CHOICES, label="Room Range")

    def clean(self):
        cleaned_data = super().clean()
        dorm = cleaned_data.get('dorm')
        room_range = cleaned_data.get('range')

        if not dorm or not room_range:
            raise forms.ValidationError("Both dorm and range must be selected.")
        
        return cleaned_data
