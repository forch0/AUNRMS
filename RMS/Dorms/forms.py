from django import forms
from .models import *


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
        
class DormForm(forms.ModelForm):
    class Meta:
        model = Dorm
        fields = ['name', 'address', 'gender', 'campus_status']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 2}),
        }

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['number', 'capacity', 'room_plan', 'floor', 'dorm', 'range']
        widgets = {
            'range': forms.Select(attrs={'class': 'form-control'}),
        }

class StorageForm(forms.ModelForm):
    class Meta:
        model = Storage
        fields = ['description', 'capacity', 'floor', 'dorm']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2}),
        }

class StorageItemForm(forms.ModelForm):
    class Meta:
        model = StorageItem
        fields = fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2}),
            'approval_date': forms.DateInput(attrs={'type': 'date'}),
            'collected_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

        # Override the __init__ method to add the search functionality
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['room'].queryset = Room.objects.all()  # Adjust the queryset if necessary
        self.fields['room'].widget.attrs.update({'class': 'select2'})  # Optional: use a JavaScript library for a better UI



class StorageItemApprovalForm(forms.ModelForm):
    class Meta:
        model = StorageItem
        fields = ['description', 'quantity', 'status']  # Include fields you want to be editable

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].widget = forms.HiddenInput()  # Status field will be set programmatically
        self.fields['description'].widget.attrs.update({'readonly': 'readonly'})
        self.fields['quantity'].widget.attrs.update({'readonly': 'readonly'})
        
    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')

        if status and status != StorageItem.APPROVED:
            raise forms.ValidationError("The status must be set to approved when saving.")
        
        return cleaned_data