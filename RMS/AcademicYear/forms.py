from django import forms
from .models import Semester

class SemesterForm(forms.ModelForm):
    class Meta:
        model = Semester
        fields = ['semester_type', 'start_date', 'end_date', 'academic_session']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
