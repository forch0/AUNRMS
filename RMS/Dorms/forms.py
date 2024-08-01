from django import forms

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
