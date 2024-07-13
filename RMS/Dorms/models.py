import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid
from django.db import models

class Dorm(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    ]

    ON_CAMPUS = 'ON'
    OFF_CAMPUS = 'OFF'
    CAMPUS_STATUS_CHOICES = [
        (ON_CAMPUS, 'On Campus'),
        (OFF_CAMPUS, 'Off Campus'),
    ]

    id = models.AutoField(primary_key=True)
    # uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default=MALE)
    campus_status = models.CharField(max_length=3, choices=CAMPUS_STATUS_CHOICES, default=ON_CAMPUS)
    capacity = models.IntegerField(default=0, help_text='Total capacity of the dorm')

    def __str__(self):
        return self.name

class Room(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    number = models.CharField(max_length=20)
    capacity = models.IntegerField()
    floor = models.IntegerField()
    dorm = models.ForeignKey(Dorm, on_delete=models.CASCADE, related_name='rooms')

    def __str__(self):
        return f"Room {self.number} - {self.dorm.name}"

class Storage(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    description = models.TextField()
    capacity = models.IntegerField()
    current_capacity = models.IntegerField(default=0)
    dorm = models.ForeignKey(Dorm, on_delete=models.CASCADE, related_name='storages')

    def __str__(self):
        return f"Storage {self.id} in {self.dorm.name}"

class StorageItem(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    description = models.TextField()
    quantity = models.IntegerField()
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE, related_name='items')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='items', blank=True, null=True)

    def __str__(self):
        return f"{self.quantity} of {self.description} in Storage {self.storage.id} - {self.storage.dorm.name}"
