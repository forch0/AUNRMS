# from django.contrib.auth.backends import BaseBackend
# from django.utils import timezone
# from .models import UserCred, Residents
# from AcademicYear.models import Enrollment, AcademicSession, Semester
# import logging

# # Set up logging
# logger = logging.getLogger(__name__)

# class StaffBackend(BaseBackend):
#     def authenticate(self, request, email=None, password=None, **kwargs):
#         if email is None or password is None:
#             logger.warning("Authentication failed: Email or password is None.")
#             return None
#         try:
#             # Fetch staff user by email
#             user = UserCred.objects.get(email=email, is_staff=True)
#             # Check if the password is correct
#             if user.check_password(password):
#                 return user
#         except UserCred.DoesNotExist:
#             logger.warning(f"Authentication failed: Staff user with email {email} does not exist.")
#         return None


# class ResidentBackend(BaseBackend):
#     def authenticate(self, request, email=None, password=None, **kwargs):
#         if email is None or password is None:
#             logger.warning("Authentication failed: Email or password is None.")
#             return None
#         try:
#             # Fetch the user by email
#             user = UserCred.objects.get(email=email)
#             # Check if the password is correct
#             if user.check_password(password):
#                 # Ensure the user is a resident
#                 resident = Residents.objects.get(user=user)
                
#                 # Get the current date
#                 current_date = timezone.now().date()

#                 # Fetch the current academic session and semester
#                 current_session = AcademicSession.objects.get(start_date__lte=current_date, end_date__gte=current_date)
#                 current_semester = Semester.objects.get(session=current_session, start_date__lte=current_date, end_date__gte=current_date)

#                 # Ensure the resident is enrolled in a room for the current semester
#                 Enrollment.objects.get(resident=resident, semester=current_semester)
                
#                 # Authentication successful, return the user
#                 return user
#         except UserCred.DoesNotExist:
#             logger.warning(f"Authentication failed: User with email {email} does not exist.")
#         except Residents.DoesNotExist:
#             logger.warning(f"Authentication failed: Resident with user {email} does not exist.")
#         except Enrollment.DoesNotExist:
#             logger.warning(f"Authentication failed: Enrollment for user {email} is not active for the current semester.")
#         except AcademicSession.DoesNotExist:
#             logger.warning("Authentication failed: No active academic session found.")
#         except Semester.DoesNotExist:
#             logger.warning("Authentication failed: No active semester found.")
#         return None


# authentication_backends.py
import logging
from django.contrib.auth.backends import ModelBackend

# Configure the logger
logger = logging.getLogger('authentication')

class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        from UserProfiles.models import UserCred  # Import here to delay it
        logger.debug(f'Attempting authentication for email: {email}')
        try:
            user = UserCred.objects.get(email=email)
            if user.check_password(password):
                logger.info(f'Successful authentication for email: {email}')
                return user
            else:
                logger.warning(f'Failed password check for email: {email}')
        except UserCred.DoesNotExist:
            logger.error(f'User with email {email} does not exist')
        return None

    def get_user(self, user_id):
        from UserProfiles.models import UserCred  # Import here to delay it
        try:
            return UserCred.objects.get(pk=user_id)
        except UserCred.DoesNotExist:
            logger.error(f'User with id {user_id} does not exist')
            return None
