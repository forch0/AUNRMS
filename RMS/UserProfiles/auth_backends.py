from django.contrib.auth.backends import BaseBackend
from .models import UserCred, Residents, Enrollment

class StaffBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = UserCred.objects.get(email=email, is_staff=True)
            if user.check_password(password):
                return user
        except UserCred.DoesNotExist:
            return None

class ResidentBackend(BaseBackend):
    def authenticate(self, request, email=None, room_number=None, password=None, **kwargs):
        try:
            user = UserCred.objects.get(email=email)
            if user.check_password(password):
                # Ensure the user is a resident with an active enrollment
                resident = Residents.objects.get(user=user)
                Enrollment.objects.get(resident=resident, room__room_number=room_number)
                return user
        except (UserCred.DoesNotExist, Residents.DoesNotExist, Enrollment.DoesNotExist):
            return None
