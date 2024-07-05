import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _

class Dorm(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)
    address = models.TextField()

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
