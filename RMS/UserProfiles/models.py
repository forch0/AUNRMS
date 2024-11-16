from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models
import uuid
from django.contrib.auth.models import Permission
from django.utils.timezone import now

# Validator for phone numbers
phone_regex = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="Phone number must be entered in the format: '+234.....'. Up to 15 digits allowed."
)

# Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

# Custom User Model
class UserCred(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=255, unique=True, blank=False)
    firstname = models.CharField(max_length=150, blank=True)
    lastname = models.CharField(max_length=150, blank=True)
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True, unique=True)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    objects = UserManager()
    date_joined = models.DateTimeField(default=now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    
    @property
    def is_resident(self):
        """Returns True if the user has a related Resident object."""
        return hasattr(self, 'residents')
    
    @property
    def is_not_resident(self):
        """Returns True if the user does not have a related Resident object."""
        return not hasattr(self, 'residents')
    
    @property
    def role_name(self):
        """Returns the role name of the user if it exists."""
        if hasattr(self, 'residents'):
            return self.residents.role.name
        elif hasattr(self, 'staffs'):
            return self.staffs.role.name
        return None

    def has_role(self, role_name):
        """Check if the user has a specific role."""
        return self.role_name == role_name

# Residents Model
class Residents(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(UserCred, on_delete=models.CASCADE, related_name='residents')
    guardian_phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    address = models.CharField(max_length=40, blank=True)
    role = models.ForeignKey('Roles', on_delete=models.CASCADE)  # Link to Roles model

    def __str__(self):
        return f"Resident: {self.user.email}"

    class Meta:
        verbose_name = 'resident'
        verbose_name_plural = 'residents'
        ordering = ['user__email']

    def get_resident_info(self):
        """Returns formatted resident information."""
        return {
            'guardian_phone_number': self.guardian_phone_number,
            'address': self.address,
            'role_name': self.role.name if self.role else "No Role Assigned"
        }

# Roles Model
class Roles(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30, unique=True)
    abbreviation = models.CharField(max_length=5, blank=True, unique=True)
    permissions = models.ManyToManyField(Permission, blank=True)

    my_order = models.PositiveIntegerField(
        default=0,
        blank=False,
        null=False,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'role'
        verbose_name_plural = 'roles'
        ordering = ['my_order']

# Staffs Model
class Staffs(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(UserCred, on_delete=models.CASCADE, related_name='staffs')
    role = models.ForeignKey(Roles, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.role.name} - {self.user.email}"

    class Meta:
        verbose_name = 'staff'
        verbose_name_plural = 'staffs'
        ordering = ['user__email']
