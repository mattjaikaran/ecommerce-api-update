import uuid
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email=None, password=None, **extra_fields):
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
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
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

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.email

    def clean(self):
        super().clean()
        if User.objects.filter(email=self.email).exclude(pk=self.pk).exists():
            raise ValidationError({"email": "A user with that email already exists."})
        if User.objects.filter(username=self.username).exclude(pk=self.pk).exists():
            raise ValidationError(
                {"username": "A user with that username already exists."}
            )

    class Meta:
        ordering = ["-date_joined"]


class AbstractBaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="%(app_label)s_%(class)s_created"
    )
    updated_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="%(app_label)s_%(class)s_updated"
    )
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False) # soft delete
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="%(app_label)s_%(class)s_deleted"
    )

    class Meta:
        abstract = True
        ordering = ["-created_at"]


class CustomerFeedback(AbstractBaseModel):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="customer_feedback")
    feedback = models.TextField(max_length=500)
    rating = models.IntegerField(default=0, choices=[(1, "1 Star"), (2, "2 Stars"), (3, "3 Stars"), (4, "4 Stars"), (5, "5 Stars")])

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Customer Feedback"
        verbose_name_plural = "Customer Feedback Messages"

    def __str__(self):
        return f"{self.customer.username} - {self.feedback[:50]}"

