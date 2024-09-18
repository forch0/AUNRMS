from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models
import uuid
from django.contrib.auth.models import Permission

phone_regex = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="Phone number must be entered in the format: '+234.....'. Up to 15 digits allowed."
)

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
class UserCred(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=255,unique=True, blank=False, validators=[
        RegexValidator(
            regex=r'@aun\.edu\.ng$',
            message='Email must be from aun.edu.ng domain.',
        ),
    ])
    firstname = models.CharField(max_length=150, blank=True)
    lastname = models.CharField(max_length=150, blank=True)
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    # EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.firstname} {self.lastname}"

    def get_short_name(self):
        return self.username

    @property
    def is_resident(self):
        return hasattr(self, 'resident_profile')

    @property
    def is_staff_only(self):
        return hasattr(self, 'staff_profile') and not self.is_resident

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        ordering = ['username']

class Residents(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(UserCred, on_delete=models.CASCADE, related_name='resident_profile')
    guardian_phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)

    def __str__(self):
        return f"Resident: {self.user.username}"

    class Meta:
        verbose_name = 'resident'
        verbose_name_plural = 'residents'
        ordering = ['user__username']

class Roles(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30, unique=True)
    abbreviation = models.CharField(max_length=5, blank=True, unique=True)
    permissions = models.ManyToManyField(Permission, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'role'
        verbose_name_plural = 'roles'
        ordering = ['name']

class Staffs(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(UserCred, on_delete=models.CASCADE, related_name='staff_profile')
    role = models.ForeignKey(Roles, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.role.name} - {self.user.username}"

    def has_perm(self, perm, obj=None):
        if self.user.is_superuser:
            return True
        return self.role.permissions.filter(codename=perm.split('.')[-1]).exists()

    class Meta:
        verbose_name = 'staff'
        verbose_name_plural = 'staffs'
        ordering = ['user__username']
