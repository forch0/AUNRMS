
# from Dorms.models import Dorm, Room  # Adjust the import as per your project structure
import uuid
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from UserProfiles.models import Residents, Staffs, Roles

class AcademicSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    start_year = models.IntegerField()
    end_year = models.IntegerField()
    name = models.CharField(max_length=100, blank=True, editable=False, help_text="Automatically formatted as start_year/end_year")
    created_at = models.DateTimeField(default=timezone.now)
    

    def clean(self):
        current_year = timezone.now().year
        last_year = current_year - 1
        if self.start_year < last_year or self.start_year > current_year:
            raise ValidationError("Start year must be from at least last year to this year.")
        if self.end_year != self.start_year + 1:
            raise ValidationError("End year must be exactly one year higher than start year.")

    def save(self, *args, **kwargs):
        self.name = f"{self.start_year}/{self.end_year}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"
    
    
    

    class Meta:
        verbose_name = 'Academic Session'
        verbose_name_plural = 'Academic Sessions'

class Semester(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    FALL = 'Fall'
    SPRING = 'Spring'
    INTERSESSION = 'Intersession'
    SEMESTER_CHOICES = [
        (FALL, 'Fall'),
        (SPRING, 'Spring'),
        (INTERSESSION, 'Intersession'),
    ]
    semester_type = models.CharField(max_length=20, choices=SEMESTER_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    academic_session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    def clean(self):
        if self.start_date is None or self.end_date is None:
            raise ValidationError("Start date and end date must be provided.")
        
        if self.start_date.year != self.end_date.year:
            raise ValidationError("Semester start date and end date must be within the same year.")
        
        if self.start_date.year not in (self.academic_session.start_year, self.academic_session.end_year):
            raise ValidationError("Semester dates must fall within the academic session's start or end years.")

    def __str__(self):
        return f"{self.get_semester_type_display()} {self.start_date.year} - {self.academic_session.name}"

class Enrollment(models.Model):
    STATUS_CHOICES = [
            ('active', 'Active'),
            ('inactive', 'Inactive'),
            ('pending', 'Pending')
        ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    resident = models.ForeignKey(Residents, on_delete=models.CASCADE, related_name='enrollments')
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='enrollments')
    academic_session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE, related_name='enrollments')
    dorm = models.ForeignKey('Dorms.Dorm', on_delete=models.CASCADE, related_name='enrollments')
    room = models.ForeignKey('Dorms.Room', on_delete=models.CASCADE, related_name='enrollments')
    date_enrolled = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')  # New status field
    

    def is_active(self):
        return self.status == 'active'

    def __str__(self):
        return f"{self.resident.user.email} - {self.semester.semester_type} ({self.academic_session.name})"

    class Meta:
        unique_together = ('resident', 'semester', 'academic_session')  # Prevent duplicate enrollments

class StaffAssignment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    staff = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    dorm = models.ForeignKey('Dorms.Dorm', on_delete=models.CASCADE)
    role = models.ForeignKey(Roles, on_delete=models.CASCADE)
    academic_session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.staff} assigned to {self.dorm} for {self.semester} in {self.academic_session}"

    class Meta:
        verbose_name = 'Staff Assignment'
        verbose_name_plural = 'Staff Assignments'
        unique_together = ('staff', 'dorm', 'academic_session', 'semester')
