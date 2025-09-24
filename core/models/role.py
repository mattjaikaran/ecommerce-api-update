"""Role-based access control models."""

import uuid

from django.contrib.auth.models import Permission
from django.db import models
from django.utils import timezone

from .abstract_base import AbstractBaseModel


class Role(AbstractBaseModel):
    """Role model for RBAC."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)
    display_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    permissions = models.ManyToManyField(
        Permission, through="RolePermission", related_name="roles"
    )

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["is_active"]),
            models.Index(fields=["name", "is_active"]),
        ]

    def __str__(self):
        return self.display_name

    def add_permission(self, permission):
        """Add a permission to this role."""
        role_permission, _ = RolePermission.objects.get_or_create(
            role=self, permission=permission
        )
        return role_permission

    def remove_permission(self, permission):
        """Remove a permission from this role."""
        RolePermission.objects.filter(role=self, permission=permission).delete()

    def has_permission(self, permission):
        """Check if role has a specific permission."""
        return self.permissions.filter(id=permission.id).exists()

    def get_permissions(self):
        """Get all permissions for this role."""
        return self.permissions.filter(rolepermission__is_active=True)


class RolePermission(AbstractBaseModel):
    """Through model for Role-Permission relationship with additional metadata."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    granted_by = models.ForeignKey(
        "core.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="granted_role_permissions",
    )
    granted_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ["role", "permission"]
        ordering = ["granted_at"]
        indexes = [
            models.Index(fields=["role", "permission"]),
            models.Index(fields=["is_active"]),
            models.Index(fields=["granted_at"]),
        ]

    def __str__(self):
        return f"{self.role.name} - {self.permission.codename}"


class UserRole(AbstractBaseModel):
    """User-Role assignment model."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        "core.User", on_delete=models.CASCADE, related_name="user_roles"
    )
    role = models.ForeignKey(
        Role, on_delete=models.CASCADE, related_name="user_assignments"
    )
    assigned_by = models.ForeignKey(
        "core.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_user_roles",
    )
    assigned_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ["user", "role"]
        ordering = ["assigned_at"]
        indexes = [
            models.Index(fields=["user", "role"]),
            models.Index(fields=["is_active"]),
            models.Index(fields=["expires_at"]),
            models.Index(fields=["assigned_at"]),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.role.name}"

    def is_expired(self):
        """Check if the role assignment is expired."""
        if not self.expires_at:
            return False
        return timezone.now() > self.expires_at

    def is_valid(self):
        """Check if the role assignment is valid (active and not expired)."""
        return self.is_active and not self.is_expired()


# Predefined roles
class PredefinedRoles:
    """Constants for predefined system roles."""

    SUPERUSER = "superuser"
    ADMIN = "admin"
    MANAGER = "manager"
    STAFF = "staff"
    CUSTOMER = "customer"
    VENDOR = "vendor"
    SUPPORT = "support"

    ROLE_DEFINITIONS = {
        SUPERUSER: {
            "display_name": "Super User",
            "description": "Full system access with all permissions",
        },
        ADMIN: {
            "display_name": "Administrator",
            "description": "Administrative access to manage system settings and users",
        },
        MANAGER: {
            "display_name": "Manager",
            "description": "Management access to oversee operations and reports",
        },
        STAFF: {
            "display_name": "Staff",
            "description": "Staff access to perform daily operations",
        },
        CUSTOMER: {
            "display_name": "Customer",
            "description": "Customer access to purchase and manage orders",
        },
        VENDOR: {
            "display_name": "Vendor",
            "description": "Vendor access to manage products and inventory",
        },
        SUPPORT: {
            "display_name": "Support",
            "description": "Customer support access to help customers",
        },
    }


# Permission groups for easier management
class PermissionGroups:
    """Constants for permission groups."""

    USER_MANAGEMENT = "user_management"
    PRODUCT_MANAGEMENT = "product_management"
    ORDER_MANAGEMENT = "order_management"
    INVENTORY_MANAGEMENT = "inventory_management"
    PAYMENT_MANAGEMENT = "payment_management"
    REPORTING = "reporting"
    SYSTEM_SETTINGS = "system_settings"
    CUSTOMER_SUPPORT = "customer_support"

    GROUP_DEFINITIONS = {
        USER_MANAGEMENT: [
            "core.add_user",
            "core.change_user",
            "core.delete_user",
            "core.view_user",
            "core.add_customer",
            "core.change_customer",
            "core.delete_customer",
            "core.view_customer",
        ],
        PRODUCT_MANAGEMENT: [
            "products.add_product",
            "products.change_product",
            "products.delete_product",
            "products.view_product",
            "products.add_category",
            "products.change_category",
            "products.delete_category",
            "products.view_category",
            "products.add_brand",
            "products.change_brand",
            "products.delete_brand",
            "products.view_brand",
        ],
        ORDER_MANAGEMENT: [
            "orders.add_order",
            "orders.change_order",
            "orders.delete_order",
            "orders.view_order",
            "orders.add_orderlineitem",
            "orders.change_orderlineitem",
            "orders.delete_orderlineitem",
            "orders.view_orderlineitem",
            "orders.process_order",
            "orders.cancel_order",
            "orders.refund_order",
        ],
        INVENTORY_MANAGEMENT: [
            "products.add_inventory",
            "products.change_inventory",
            "products.view_inventory",
            "products.adjust_stock",
            "products.view_stock_reports",
        ],
        PAYMENT_MANAGEMENT: [
            "payments.add_payment",
            "payments.change_payment",
            "payments.view_payment",
            "payments.process_refund",
            "payments.view_transactions",
        ],
        REPORTING: [
            "core.view_reports",
            "orders.view_order_reports",
            "products.view_product_reports",
            "payments.view_payment_reports",
        ],
        SYSTEM_SETTINGS: [
            "core.change_settings",
            "core.view_settings",
            "core.manage_cache",
            "core.view_logs",
        ],
        CUSTOMER_SUPPORT: [
            "core.view_customer_feedback",
            "core.add_customer_feedback",
            "core.change_customer_feedback",
            "orders.view_order",
            "orders.change_order_status",
        ],
    }
