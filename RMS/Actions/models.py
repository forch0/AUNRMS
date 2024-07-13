from django.db import models
import uuid
from django.utils import timezone
from AcademicYear.models import AcademicSession, Semester  # Adjust import path as needed
from Dorms.models import Dorm  # Adjust import path as needed
from UserProfiles.models import UserCred  # Adjust import path as needed

class Announcement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(UserCred, on_delete=models.CASCADE, related_name='announcements')
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    academic_session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, null=True, blank=True)
    global_announcement = models.BooleanField(default=False)
    dorm = models.ForeignKey(Dorm, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-id']  # Order by id descending (-id) by default


class Complaint(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(UserCred, on_delete=models.CASCADE, related_name='complaints')
    title = models.CharField(max_length=100)
    description = models.TextField()
    anonymous = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    academic_session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.anonymous:
            self.user = None
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-id']  # Order by id descending (-id) by default
