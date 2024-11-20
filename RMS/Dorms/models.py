import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from AcademicYear.models import Enrollment, AcademicSession, Semester
from UserProfiles.models import Residents, Staffs
from django.utils import timezone
class Dorm(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    UNISEX = 'C'
    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (UNISEX, 'Unisex'),
    ]

    ON_CAMPUS = 'ON'
    OFF_CAMPUS = 'OFF'
    CAMPUS_STATUS_CHOICES = [
        (ON_CAMPUS, 'On Campus'),
        (OFF_CAMPUS, 'Off Campus'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default=MALE)
    campus_status = models.CharField(max_length=3, choices=CAMPUS_STATUS_CHOICES, default=ON_CAMPUS)

    def active_residents_count(self, semester):
        return Enrollment.objects.filter(room__dorm=self, semester=semester).count()

    def total_capacity(self):
        return sum(room.capacity for room in self.rooms.all())

    def is_full(self, semester):
        active_count = self.active_residents_count(semester)
        return active_count >= self.total_capacity()

    def occupancy_ratio(self, semester):
        active_count = self.active_residents_count(semester)
        total_capacity = self.total_capacity()
        return f"{active_count}/{total_capacity}"
    
    def room_count(self):
        return self.rooms.count()

    def __str__(self):
        return self.name


    # @property
    # def occupancy_ratio(self):
    #     """Return the occupancy ratio as a string in the format 'current/total'."""
    #     active_count = self.active_capacity_count(semester)  # Ensure to pass the semester appropriately
    #     return f"{active_count}/{self.capacity}"

class Room(models.Model):
    FLOOR_CHOICES = [
        (1, 'Ground Floor'),
        (2, 'First Floor'),
        (3, 'Second Floor'),
        (4, 'Third Floor'),
    ]

    ROOM_OPTIONS = [
        ('3_in_1_wof', 'Triple Without Facilities'),
        ('2_in_1_wof', 'Double Without Facilities'),
        ('3_in_1_wf', 'Triple With Facilities'),
        ('2_in_1_wf', 'Double With Facilities'),
    ]

    RANGE_CHOICES = [
        ('101-116', '101-116'),
        ('201-216', '201-216'),
        ('301-316', '301-316'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    number = models.CharField(max_length=20)
    capacity = models.IntegerField()
    room_plan = models.CharField(max_length=20, choices=ROOM_OPTIONS)
    floor = models.IntegerField(choices=FLOOR_CHOICES)
    dorm = models.ForeignKey(Dorm, on_delete=models.CASCADE, related_name='rooms')
    range = models.CharField(max_length=20, choices=RANGE_CHOICES, blank=True, null=True)
    is_occupied = models.BooleanField(default=False)

    def active_residents_count(self, semester):
        """Count active residents in this room for the given semester."""
        active_count = Enrollment.objects.filter(room=self, semester=semester, status='active').count()
        print(f"Active count for room {self.room_name}: {active_count}")  # Debugging line
        return active_count
    def update_occupation_status(self, semester):
        """Update the 'is_occupied' field based on active enrollments."""
        active_count = self.active_residents_count(semester)
        self.is_occupied = active_count > 0
        self.save()

    def __str__(self):
        return f"Room {self.number} - {self.dorm.name}"

    @property
    def room_name(self):
        """Return a formatted string of room and dorm name."""
        return f"{self.dorm.name}-{self.number}"

    @property
    def occupancy_ratio(self, semester):
        """Return the occupancy ratio as 'active_count/capacity'."""
        active_count = self.active_residents_count(semester)
        return f"{active_count}/{self.capacity}"

    def save(self, *args, **kwargs):
        """Override the save method to dynamically set the 'is_occupied' field."""
        semester = Semester.objects.first()  # Assuming first semester if not specified
        if semester:
            self.update_occupation_status(semester)
        super().save(*args, **kwargs)


class Storage(models.Model):
    FLOOR_CHOICES = [
        (1, 'Ground Floor'),
        (2, 'First Floor'),
        (3, 'Second Floor'),
        (4, 'Third Floor'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField()
    capacity = models.IntegerField()
    floor = models.IntegerField(choices=FLOOR_CHOICES)
    current_capacity = models.IntegerField(default=0)
    dorm = models.ForeignKey(Dorm, on_delete=models.CASCADE, related_name='storages')

    def __str__(self):
        return f"Storage {self.id} in {self.dorm.name}"
    
    class Meta:
        verbose_name = 'Storage Location'
        verbose_name_plural = 'Storage Locations'

class StorageItem(models.Model):
    PENDING = 'P'
    APPROVED = 'A'
    REJECTED = 'R'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField()
    quantity = models.IntegerField()
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE, related_name='items')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='items', blank=True, null=True)
    resident = models.ForeignKey(Residents, on_delete=models.CASCADE, related_name='storage_items')
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='storage_items')
    academic_session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE, related_name='storage_items')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=PENDING)
    approved_by = models.ForeignKey(Staffs, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_storage_items')
    approval_date = models.DateField(null=True, blank=True)
    collected_at = models.DateTimeField(null=True, blank=True)  # Date and time when collected
    collected_by = models.ForeignKey(Residents, on_delete=models.SET_NULL, null=True, blank=True, related_name='collected_items')
    created_at = models.DateTimeField(default=timezone.now)
    class Meta:
        verbose_name = 'Storage Item'
        verbose_name_plural = 'Storage Items'

    def approve(self, staff_member):
        allowed_roles = ['Residence Assistant', 'Residence Director']  # List of allowed role names

        if staff_member.role.name in allowed_roles:
            self.status = StorageItem.APPROVED
            self.approved_by = staff_member
            self.approval_date = timezone.now()
            self.save()
        else:
            raise PermissionError("Staff member does not have permission to approve storage items.")
        
    def __str__(self):
        return f"Storage Item: {self.description} (Quantity: {self.quantity}) - Resident: {self.resident.name} - Status: {self.get_status_display()}"
