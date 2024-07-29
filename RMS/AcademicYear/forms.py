from django import forms
from .models import Semester

class SemesterForm(forms.ModelForm):
    class Meta:
        model = Semester
        fields = ['semester_type', 'start_date', 'end_date', 'academic_session']
        widgets = {
            'start_date': forms.DateInput(attrs={'class': 'form-control datepicker', 'placeholder': 'YYYY-MM-DD'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control datepicker', 'placeholder': 'YYYY-MM-DD'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        academic_session = cleaned_data.get('academic_session')

        if start_date and end_date:
            if start_date.year != end_date.year:
                self.add_error('end_date', "Semester start date and end date must be within the same year.")
            if academic_session:
                if start_date.year not in (academic_session.start_year, academic_session.end_year):
                    self.add_error('start_date', "Semester dates must fall within the academic session's start or end years.")
        
        return cleaned_data