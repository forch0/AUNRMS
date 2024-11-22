from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
import uuid
from cryptography.fernet import Fernet
from AcademicYear.models import AcademicSession, Semester,Enrollment  # Adjust import path as needed
from Dorms.models import Dorm, Room 
from UserProfiles.models import Staffs,Residents  # Adjust import path as needed

key = Fernet.generate_key()
cipher = Fernet(key)

class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20, unique=True)
    

    def __str__(self):
        return self.name
    
    my_order = models.PositiveIntegerField(
        default=0,
        blank=False,
        null=False,

    )
    
    class Meta:
        verbose_name = 'Maintenance-Category'
        verbose_name_plural = 'Maintenance-Categories'

class SubCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')

    my_order = models.PositiveIntegerField(
        default=0,
        blank=False,
        null=False,

    )

    def __str__(self):
        return f"{self.name} ({self.category.name})"
    
    class Meta:
        verbose_name = 'Maintenance-Sub-Category'
        verbose_name_plural = 'Maintenance-Sub-Categories'

class MaintenanceRequest(models.Model):

    PENDING = 'P'
    IN_PROGRESS = 'IP'
    COMPLETED = 'C'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (IN_PROGRESS, 'In Progress'),
        (COMPLETED, 'Completed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dorm = models.ForeignKey('Dorms.Dorm', on_delete=models.CASCADE, related_name='maintenance_requests')
    room = models.ForeignKey('Dorms.Room', on_delete=models.CASCADE, related_name='maintenance_requests', blank=True, null=True)
    resident = models.ForeignKey(Residents, on_delete=models.CASCADE, related_name='maintenance_requests')
    semester = models.ForeignKey('AcademicYear.Semester', on_delete=models.CASCADE, related_name='maintenance_requests')
    academic_session = models.ForeignKey('AcademicYear.AcademicSession', on_delete=models.CASCADE, related_name='maintenance_requests')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(Staffs, on_delete=models.SET_NULL, null=True, blank=True, related_name='updated_requests')
    updated_at = models.DateTimeField(auto_now=True)
    completion_date = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.status == self.COMPLETED and self.completion_date is None:
            self.completion_date = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Request {self.id} by {self.resident.user.email} - {self.status}"
    
    class Meta:
        verbose_name = 'Maintenance Request'
        verbose_name_plural = 'Maintenance Requests'
    
# class Announcement(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     title = models.CharField(max_length=200)
#     message = models.TextField(blank=True, null=True)
#     created_by = models.ForeignKey(Staffs, on_delete=models.CASCADE, related_name='created_announcements')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     dorms = models.ManyToManyField(Dorm, blank=True)  # For ResLife Director's global announcements
#     is_global = models.BooleanField(default=False)
#     semester = models.ForeignKey('AcademicYear.Semester', on_delete=models.CASCADE, related_name='announcements')
#     academic_session = models.ForeignKey('AcademicYear.AcademicSession', on_delete=models.CASCADE, related_name='announcements')

#     def clean(self):
#         if self.is_global:
#             if self.created_by.role.name != 'ResLife Director':
#                 raise ValidationError("Only ResLife Directors can make global announcements.")
#         else:
#             if not self.dorms.exists():
#                 raise ValidationError("Announcements must be assigned to a dorm.")
#             for dorm in self.dorms.all():
#                 if self.created_by.dorm != dorm and self.created_by.role.name not in ['Residence Director', 'Residence Assistant']:
#                     raise ValidationError("You can only create announcements for the dorm you are assigned to.")

#     def __str__(self):
#         return f"{self.title} by {self.created_by.user.username}"

#     class Meta:
#         verbose_name = 'announcement'
#         verbose_name_plural = 'announcements'

class Announcement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    message = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(
        Staffs, 
        on_delete=models.CASCADE, 
        related_name='created_announcements'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    dorms = models.ManyToManyField(
        Dorm, 
        blank=True, 
        help_text="Select dorms for the announcement (Leave blank for global announcements)."
    )
    is_global = models.BooleanField(default=False)
    semester = models.ForeignKey(
        Semester, 
        on_delete=models.CASCADE, 
        related_name='announcements'
    )
    academic_session = models.ForeignKey(
        AcademicSession, 
        on_delete=models.CASCADE, 
        related_name='announcements'
    )

    class Meta:
        verbose_name = "Announcement"
        verbose_name_plural = "Announcements"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Complaint(models.Model):

    COMPLAINT_TYPE_CHOICES = [
            ('wifi', 'Wi-Fi'),
            ('television', 'Television'),
            ('noise', 'Noise Complaint'),
            ('fight', 'Physical Abuse'),
            ('sex', 'Sexual Abuse'),
            ('drug', 'Drugs'),
            ('residence staff', 'Residence Staffs'),
            ('cleaners', 'Cleaning Staffs'),

    ]

    STATUS_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('pending', 'Pending'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='complaints', null=True, blank=True)
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='complaints')
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='complaints')
    academic_session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE, related_name='complaints')
    complaint_type = models.CharField(max_length=20, choices=COMPLAINT_TYPE_CHOICES)
    description = models.TextField()
    is_anonymous = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')
    
    def save(self, *args, **kwargs):
        if self.is_anonymous:
            self.description = cipher.encrypt(self.description.encode()).decode()
        super().save(*args, **kwargs)

    def get_description(self):
        if self.is_anonymous:
            return "This complaint is anonymous."
        return self.description

    def decrypt_description(self):
        """Decrypt the description if it's an anonymous complaint."""
        if self.is_anonymous:
            return cipher.decrypt(self.description.encode()).decode()
        return self.description

    def __str__(self):
        user_name = self.user.email if self.user else 'Anonymous'  # Safely check if user exists
        return f"Complaint by {user_name} - {self.id}"
        
    class Meta:
        verbose_name = 'complaint'
        verbose_name_plural = 'complaints'

class Vendor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    business_name = models.CharField(max_length=200)
    owner_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=15)
    dorm = models.ForeignKey(Dorm, on_delete=models.CASCADE, null=True, blank=True, related_name='vendors')
    is_off_campus = models.BooleanField(default=False)  # If the vendor is off-campus
    product = models.CharField(max_length=200)  # A description or name of the product

    def __str__(self):
        return f"{self.business_name} by {self.owner_name}"

    class Meta:
        verbose_name = 'Vendor'
        verbose_name_plural = 'Vendors'