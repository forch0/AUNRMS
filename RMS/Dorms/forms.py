from django import forms

class GenerateRoomsForm(forms.Form):
    ranges = forms.MultipleChoiceField(
        choices=[
            ('101-116', '101-116'),
            ('201-216', '201-216'),
            ('301-316', '301-316'),
            ('2x2a-2x2b', '2x2a-2x2b'),
            ('3x3a-3x3b', '3x3a-3x3b'),
        ],
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
