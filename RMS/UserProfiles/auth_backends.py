from django.contrib.auth.backends import ModelBackend
from .models import UserCred, Staff, Resident

class StaffBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserCred.objects.get(username=username, is_staff=True)
            if user.check_password(password):
                return user
        except UserCred.DoesNotExist:
            return None

class ResidentBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserCred.objects.get(username=username, is_staff=False)
            if user.check_password(password):
                return user
        except UserCred.DoesNotExist:
            return None
