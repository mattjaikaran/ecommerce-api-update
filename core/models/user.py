"""User model and manager definition."""

import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager, Permission, PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


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
            raise ValidationError(e.message_dict) from e
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

    # RBAC Methods
    def assign_role(self, role, assigned_by=None, expires_at=None):
        """Assign a role to this user."""
        from .role import UserRole

        user_role, _ = UserRole.objects.get_or_create(
            user=self,
            role=role,
            defaults={
                "assigned_by": assigned_by,
                "expires_at": expires_at,
                "is_active": True,
            },
        )
        return user_role

    def remove_role(self, role):
        """Remove a role from this user."""
        from .role import UserRole

        UserRole.objects.filter(user=self, role=role).delete()

    def has_role(self, role_name):
        """Check if user has a specific role."""
        from .role import UserRole

        return UserRole.objects.filter(
            user=self, role__name=role_name, is_active=True
        ).exists()

    def get_roles(self):
        """Get all active roles for this user."""
        from .role import Role

        return Role.objects.filter(
            user_assignments__user=self, user_assignments__is_active=True
        )

    def get_role_permissions(self):
        """Get all permissions from assigned roles."""
        # Get permissions from active, non-expired roles
        return (
            Permission.objects.filter(
                roles__user_assignments__user=self,
                roles__user_assignments__is_active=True,
                rolepermission__is_active=True,
            )
            .filter(
                models.Q(roles__user_assignments__expires_at__isnull=True)
                | models.Q(roles__user_assignments__expires_at__gt=timezone.now())
            )
            .distinct()
        )

    def has_permission(self, permission_codename):
        """Check if user has a specific permission (including role-based)."""
        # Check Django's built-in permission system first
        if super().has_perm(permission_codename):
            return True

        # Check role-based permissions
        return self.get_role_permissions().filter(codename=permission_codename).exists()

    def get_all_permissions(self):
        """Get all permissions for this user (Django + role-based)."""
        # Get Django permissions
        django_perms = set(self.get_all_permissions_from_groups_and_user())

        # Get role-based permissions
        role_perms = set(perm.codename for perm in self.get_role_permissions())

        return django_perms | role_perms

    def is_admin(self):
        """Check if user is an admin (staff or has admin role)."""
        return self.is_staff or self.has_role("admin") or self.has_role("superuser")

    def is_manager(self):
        """Check if user is a manager."""
        return self.is_admin() or self.has_role("manager")

    def is_customer_user(self):
        """Check if user is a customer."""
        return self.has_role("customer")

    def is_vendor_user(self):
        """Check if user is a vendor."""
        return self.has_role("vendor")

    def is_support_user(self):
        """Check if user is a support agent."""
        return self.has_role("support") or self.is_admin()

    def can_manage_users(self):
        """Check if user can manage other users."""
        return (
            self.is_superuser
            or self.has_permission("core.change_user")
            or self.has_role("admin")
        )

    def can_manage_products(self):
        """Check if user can manage products."""
        return (
            self.is_admin()
            or self.has_permission("products.change_product")
            or self.has_role("vendor")
        )

    def can_manage_orders(self):
        """Check if user can manage orders."""
        return (
            self.is_admin()
            or self.has_permission("orders.change_order")
            or self.has_role("manager")
        )

    def can_view_reports(self):
        """Check if user can view reports."""
        return (
            self.is_admin()
            or self.has_permission("core.view_reports")
            or self.has_role("manager")
        )
