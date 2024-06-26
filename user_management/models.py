from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.base_user import AbstractBaseUser


# Create your models here.
class UserModuleManager(BaseUserManager):
    use_in_migrations = True 

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        email, password, False, **data
        """
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(str(password))
        user.is_active = False
        user.save()
        created = True
        return user, created

    def create_user(self, phone, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone, email, (str(password)), **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, (str(password)), **extra_fields)
class User(AbstractBaseUser):
    """creates a usermodel that supports email address instead of username"""

    class Meta:
        db_table = 'user_manager'

    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    country_code = models.CharField(max_length=255)
    email = models.CharField(max_length=100, unique=True)
    phone = models.CharField(max_length=255, default=False)
    date_activated = models.DateTimeField(auto_now_add=True)
    password = models.CharField(max_length=255, default=False)    
    last_name = models.CharField(max_length=255, default=False)
    first_name = models.CharField(max_length=255, default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserModuleManager()
    