# your_app_name/models.py

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        """
        Creates and saves a User with the given username and password.
        """
        if not username:
            raise ValueError('The Username must be set')
        email = self.normalize_email(email)
        if not email.endswith('@aun.edu.ng'):
            raise ValueError('Email must be from aun.edu.ng domain.')
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given username and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)

class UserCred(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=255, blank=False, validators=[
        RegexValidator(
            regex=r'@aun\.edu\.ng$',
            message='Email must be from aun.edu.ng domain.',
        ),
    ], default='aun@example.com')  # Provide a default email
    firstname = models.CharField(max_length=150, blank=True)
    lastname = models.CharField(max_length=150, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    def get_full_name(self):
        return f"{self.firstname} {self.lastname}"

    def get_short_name(self):
        return self.username

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

class Resident(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(UserCred, on_delete=models.CASCADE, related_name='resident_profile')

    def __str__(self):
        return f"Resident: {self.user.username}"

    class Meta:
        verbose_name = 'resident'
        verbose_name_plural = 'residents'

class Role(models.Model):
    name = models.CharField(max_length=20, unique=True)
    abbreviation = models.CharField(max_length=5, blank=True, unique=True)

    def __str__(self):
        return self.name

class Staff(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(UserCred, on_delete=models.CASCADE, related_name='staff_profile')
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.role.name} - {self.user.username}"

    class Meta:
        verbose_name = 'staff'
        verbose_name_plural = 'staffs'
