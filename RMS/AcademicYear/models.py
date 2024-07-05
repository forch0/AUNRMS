from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

class AcademicSession(models.Model):
    id = models.AutoField(primary_key=True)
    start_year = models.IntegerField()
    end_year = models.IntegerField()
    name = models.CharField(max_length=100, blank=True, editable=False, help_text="Automatically formatted as start_year/end_year")

    def clean(self):
        if self.start_year >= timezone.now().year:
            raise ValidationError("Start year must be at least one year before the current year.")
        if self.end_year != self.start_year + 1:
            raise ValidationError("End year must be exactly one year higher than start year.")

    def save(self, *args, **kwargs):
        self.name = f"{self.start_year}/{self.end_year}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"

class Semester(models.Model):
    id = models.AutoField(primary_key=True)
    FALL = 'Fall'
    SPRING = 'Spring'
    SUMMER = 'Summer'
    SEMESTER_CHOICES = [
        (FALL, 'Fall'),
        (SPRING, 'Spring'),
        (SUMMER, 'Summer'),
    ]
    semester_type = models.CharField(max_length=10, choices=SEMESTER_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    academic_session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)

    def clean(self):
        if self.start_date.year != self.academic_session.start_year or self.end_date.year != self.academic_session.end_year:
            raise ValidationError("Semester dates must fall within the academic session's start and end years.")

    def __str__(self):
        return f"{self.get_semester_type_display()} {self.start_date.year}/{self.end_date.year} - {self.academic_session.name}"
