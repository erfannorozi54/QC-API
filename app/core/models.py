"""
Database models.
"""
import uuid

import os

from django.core.validators import validate_ipv46_address
from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.validators import MinValueValidator, MaxValueValidator


def image_file_path(instance, filename):
    """Generate file path for new recipe image"""
    ext = os.path.splitext(filename)[1]
    filename = f'{instance.created_at}_{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'recipe', filename)


class UserManager(BaseUserManager): 
    """Maneger for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return new user."""
        if not email:
            raise ValueError('User must have an email address.')
        user = self.mdodel(email.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, email, password):
        """create and return a new superuser."""
        user = self.create_user(email=email,password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class ProductionLine(models.Model):
    """Production line object"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=255,)
    product = models.CharField(max_length=255,)


    def __str__(self):
        return f'{self.name} producting {self.product}'
    

class Camera(models.Model):
    """Camera object"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cameras',
    )
    product_line = models.ForeignKey(
        'ProductionLine',
        on_delete=models.CASCADE,
        related_name='cameras'
    )
    IP = models.GenericIPAddressField(
        validators=[validate_ipv46_address],
        help_text="IP address of the camera"
    )
    username = models.CharField(max_length=255, help_text="Username for camera access")
    password = models.CharField(max_length=255, help_text="Password for camera access")

    def __str__(self):
        return f"Camera at {self.ip_address}"


class Item(models.Model):
    """Represents an object that is photographed from multiple angles"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    index = models.BigIntegerField()
    
    def __str__(self):
        return f"Item {self.id}"
    

class Image(models.Model):
    """Image object captured by a camera."""
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name='images',
        help_text="The item this image represents"
    )
    camera = models.ForeignKey(
        'Camera',
        on_delete=models.DO_NOTHING,
        related_name='images',
        help_text="The camera that captured this image"
    )
    grade = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(3)],
        help_text="Grade of the image (0-100)"
    )
    capture_time = models.DateTimeField(help_text="Date and time when the image was captured")
    
    # Additional fields
    image = models.ImageField(null=True, upload_to=image_file_path)
    # file_size = models.PositiveIntegerField(help_text="Size of the image file in bytes")
    # resolution = models.CharField(max_length=20, help_text="Image resoltion, e.g., '1920x1080'")
    
    # Metadata fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the record was created")

    def __str__(self):
        return f"Image of {self.item}"

    class Meta:
        ordering = ['-capture_time']
        verbose_name = "Image"
        verbose_name_plural = "Images"
        unique_together = ['item', 'camera']