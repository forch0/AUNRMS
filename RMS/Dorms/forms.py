from django import forms
from .models import Dorm

class RoomGenerationForm(forms.Form):
    dorm = forms.ModelChoiceField(queryset=Dorm.objects.all())
    range = forms.ChoiceField(
        choices=[
            ('101-116', '101-116'),
            ('201-216', '201-216'),
            ('301-316', '301-316'),
        ],
        required=False
    )
    range_start = forms.IntegerField(required=False)
    range_end = forms.IntegerField(required=False)
    capacity = forms.IntegerField()
    room_plan = forms.CharField()
    floor = forms.CharField()
