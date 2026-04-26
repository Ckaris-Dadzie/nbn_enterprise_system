# accounts/models.py
import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from core.utils import SoftDeleteMixin

# Role
class Role(models.Model):
    name        = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, default='')
    created_at  = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name


    class Meta:
        ordering = ['name']



# Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user  = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff',     True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)



# User
class User(AbstractBaseUser, PermissionsMixin, SoftDeleteMixin):
    # UUID4 primary key — only model in the system with UUID PK
    id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email       = models.EmailField(unique=True)
    username    = models.CharField(max_length=150, unique=True)
    full_name   = models.CharField(max_length=255)
    role        = models.ForeignKey(
                      Role,
                      on_delete=models.PROTECT,
                      null=True,
                      blank=True,
                  )
    is_staff    = models.BooleanField(default=False)
    created_at  = models.DateTimeField(auto_now_add=True)
    created_by  = models.ForeignKey(
                      'self',
                      null=True,
                      blank=True,
                      on_delete=models.SET_NULL,
                      related_name='created_users',
                  )
    updated_at = models.DateTimeField(auto_now=True)


    objects = UserManager()


    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['username', 'full_name']


    def __str__(self):
        return f'{self.full_name} ({self.email})'


    class Meta:
        ordering = ['full_name']



# AuditLog
class AuditLog(models.Model):
    user        = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action      = models.CharField(max_length=100)
    resource    = models.CharField(max_length=100)
    resource_id = models.CharField(max_length=50)
    details     = models.JSONField(default=dict)
    ip_address  = models.GenericIPAddressField(null=True, blank=True)
    timestamp   = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.action} by {self.user} at {self.timestamp}'


    class Meta:
        ordering = ['-timestamp']
