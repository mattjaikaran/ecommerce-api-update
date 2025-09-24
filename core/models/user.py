"""User model and manager definition."""

import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models


class CustomUserManager(BaseUserManager):
    """Custom user manager for handling email-based authentication."""

    use_in_migrations = True

    def create_user(self, email=None, password=None, **extra_fields):
        """Create and save a regular user with email and password."""
        if not email:
            raise ValueError("The Email field must be set")
        normalized_email = self.normalize_email(email).lower()

        user = self.model(email=normalized_email, **extra_fields)
        user.set_password(password)
        try:
            user.save(using=self._db)
        except ValidationError as e:
            raise ValidationError(e.message_dict)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a superuser with email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model with email-based authentication."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True)
    username = models.CharField(max_length=50, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = CustomUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "first_name", "last_name"]

    class Meta:
        ordering = ["-date_joined"]
        indexes = [
            # Core lookup indexes
            models.Index(fields=["email"]),
            models.Index(fields=["username"]),
            models.Index(fields=["is_staff"]),
            models.Index(fields=["is_superuser"]),
            models.Index(fields=["date_joined"]),
            # Compound indexes for common queries
            models.Index(fields=["is_staff", "is_superuser"]),
            models.Index(fields=["email", "is_staff"]),
        ]

    def __str__(self):
        return f"{self.full_name} - {self.email}"

    @property
    def full_name(self):
        """Return the user's full name."""
        return f"{self.first_name} {self.last_name}"

    def clean(self):
        """Validate the user data."""
        super().clean()
        if User.objects.filter(email=self.email).exclude(pk=self.pk).exists():
            raise ValidationError({"email": "A user with that email already exists."})
        if User.objects.filter(username=self.username).exclude(pk=self.pk).exists():
            raise ValidationError(
                {"username": "A user with that username already exists."}
            )
