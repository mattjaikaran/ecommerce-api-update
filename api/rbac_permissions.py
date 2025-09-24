"""Role-based access control permission classes."""

from collections.abc import Callable
from functools import wraps
from typing import Any

from django.http import HttpRequest
from ninja_extra.permissions import BasePermission

from .exceptions import APIPermissionError, AuthenticationError


class RoleBasedPermission(BasePermission):
    """Base class for role-based permissions."""

    required_roles = []
    required_permissions = []

    def has_permission(self, request: HttpRequest, view: Any) -> bool:
        """Check if user has required roles or permissions."""
        if not request.user or not request.user.is_authenticated:
            return False

        # Superusers have all permissions
        if request.user.is_superuser:
            return True

        # Check roles
        if self.required_roles:
            user_has_role = any(
                request.user.has_role(role) for role in self.required_roles
            )
            if user_has_role:
                return True

        # Check permissions
        if self.required_permissions:
            user_has_permission = any(
                request.user.has_permission(perm) for perm in self.required_permissions
            )
            if user_has_permission:
                return True

        return False


class IsSuperUser(RoleBasedPermission):
    """Permission that requires superuser or superuser role."""

    required_roles = ["superuser"]

    def has_permission(self, request: HttpRequest, view: Any) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.is_superuser or request.user.has_role("superuser")


class IsAdmin(RoleBasedPermission):
    """Permission that requires admin role or staff status."""

    required_roles = ["admin", "superuser"]

    def has_permission(self, request: HttpRequest, view: Any) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False
        return (
            request.user.is_staff
            or request.user.is_superuser
            or request.user.has_role("admin")
            or request.user.has_role("superuser")
        )


class IsManager(RoleBasedPermission):
    """Permission that requires manager role or higher."""

    required_roles = ["manager", "admin", "superuser"]


class IsStaff(RoleBasedPermission):
    """Permission that requires staff role or higher."""

    required_roles = ["staff", "manager", "admin", "superuser"]


class IsCustomer(RoleBasedPermission):
    """Permission that requires customer role."""

    required_roles = ["customer"]


class IsVendor(RoleBasedPermission):
    """Permission that requires vendor role."""

    required_roles = ["vendor"]


class IsSupport(RoleBasedPermission):
    """Permission that requires support role or higher."""

    required_roles = ["support", "manager", "admin", "superuser"]


# Permission classes for specific actions
class CanManageUsers(RoleBasedPermission):
    """Permission to manage users."""

    required_roles = ["admin", "superuser"]
    required_permissions = ["core.add_user", "core.change_user", "core.delete_user"]


class CanManageProducts(RoleBasedPermission):
    """Permission to manage products."""

    required_roles = ["vendor", "manager", "admin", "superuser"]
    required_permissions = ["products.add_product", "products.change_product"]


class CanManageOrders(RoleBasedPermission):
    """Permission to manage orders."""

    required_roles = ["staff", "manager", "admin", "superuser"]
    required_permissions = ["orders.change_order", "orders.process_order"]


class CanManageInventory(RoleBasedPermission):
    """Permission to manage inventory."""

    required_roles = ["vendor", "staff", "manager", "admin", "superuser"]
    required_permissions = ["products.change_inventory", "products.adjust_stock"]


class CanManagePayments(RoleBasedPermission):
    """Permission to manage payments."""

    required_roles = ["manager", "admin", "superuser"]
    required_permissions = ["payments.change_payment", "payments.process_refund"]


class CanViewReports(RoleBasedPermission):
    """Permission to view reports."""

    required_roles = ["manager", "admin", "superuser"]
    required_permissions = ["core.view_reports"]


class CanManageSettings(RoleBasedPermission):
    """Permission to manage system settings."""

    required_roles = ["admin", "superuser"]
    required_permissions = ["core.change_settings"]


class CanProvideSupport(RoleBasedPermission):
    """Permission to provide customer support."""

    required_roles = ["support", "manager", "admin", "superuser"]
    required_permissions = ["core.view_customer_feedback", "orders.view_order"]


# Ownership-based permissions
class IsOwnerOrAdmin(BasePermission):
    """Permission that requires ownership or admin access."""

    def has_object_permission(self, request: HttpRequest, view: Any, obj: Any) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False

        # Check if user is admin
        if request.user.is_admin():
            return True

        # Check ownership
        return self._is_owner(request.user, obj)

    def _is_owner(self, user, obj):
        """Check if user owns the object."""
        if hasattr(obj, "user"):
            return obj.user == user
        if hasattr(obj, "owner"):
            return obj.owner == user
        if hasattr(obj, "customer") and hasattr(obj.customer, "user"):
            return obj.customer.user == user
        return False


class IsOwnerOrManager(IsOwnerOrAdmin):
    """Permission that requires ownership or manager access."""

    def has_object_permission(self, request: HttpRequest, view: Any, obj: Any) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False

        # Check if user is manager or admin
        if request.user.is_manager():
            return True

        # Check ownership
        return self._is_owner(request.user, obj)


class IsOwnerOrSupport(IsOwnerOrAdmin):
    """Permission that requires ownership or support access."""

    def has_object_permission(self, request: HttpRequest, view: Any, obj: Any) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False

        # Check if user is support, manager or admin
        if request.user.is_support_user():
            return True

        # Check ownership
        return self._is_owner(request.user, obj)


# Decorators for role-based access control
def require_role(*required_roles) -> Callable:
    """Decorator that requires user to have specific roles."""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Find request object
            request = None
            for arg in args:
                if hasattr(arg, "user") and hasattr(arg, "META"):
                    request = arg
                    break
                if hasattr(arg, "request"):
                    request = arg.request
                    break

            if not request or not request.user or not request.user.is_authenticated:
                raise AuthenticationError("Authentication required")

            # Check if user has any of the required roles
            if not any(request.user.has_role(role) for role in required_roles):
                role_list = ", ".join(required_roles)
                raise APIPermissionError(f"Required role(s): {role_list}")

            return func(*args, **kwargs)

        return wrapper

    return decorator


def require_permission(*required_permissions) -> Callable:
    """Decorator that requires user to have specific permissions."""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Find request object
            request = None
            for arg in args:
                if hasattr(arg, "user") and hasattr(arg, "META"):
                    request = arg
                    break
                if hasattr(arg, "request"):
                    request = arg.request
                    break

            if not request or not request.user or not request.user.is_authenticated:
                raise AuthenticationError("Authentication required")

            # Check if user has any of the required permissions
            if not any(
                request.user.has_permission(perm) for perm in required_permissions
            ):
                perm_list = ", ".join(required_permissions)
                raise APIPermissionError(f"Required permission(s): {perm_list}")

            return func(*args, **kwargs)

        return wrapper

    return decorator


def require_admin(func: Callable) -> Callable:
    """Decorator that requires admin access."""
    return require_role("admin", "superuser")(func)


def require_manager(func: Callable) -> Callable:
    """Decorator that requires manager access or higher."""
    return require_role("manager", "admin", "superuser")(func)


def require_staff(func: Callable) -> Callable:
    """Decorator that requires staff access or higher."""
    return require_role("staff", "manager", "admin", "superuser")(func)


def require_customer(func: Callable) -> Callable:
    """Decorator that requires customer role."""
    return require_role("customer")(func)


def require_vendor(func: Callable) -> Callable:
    """Decorator that requires vendor role."""
    return require_role("vendor")(func)


def require_support(func: Callable) -> Callable:
    """Decorator that requires support role or higher."""
    return require_role("support", "manager", "admin", "superuser")(func)


# Combined decorators for common patterns
def admin_or_owner_required(obj_param: str = "obj") -> Callable:
    """Decorator that requires admin access or ownership."""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Find request object
            request = None
            for arg in args:
                if hasattr(arg, "user") and hasattr(arg, "META"):
                    request = arg
                    break
                if hasattr(arg, "request"):
                    request = arg.request
                    break

            if not request or not request.user or not request.user.is_authenticated:
                raise AuthenticationError("Authentication required")

            # Check if user is admin
            if request.user.is_admin():
                return func(*args, **kwargs)

            # Check ownership
            obj = kwargs.get(obj_param)
            if not obj:
                raise APIPermissionError("Object not found")

            permission = IsOwnerOrAdmin()
            if not permission.has_object_permission(request, None, obj):
                raise APIPermissionError(
                    "Access denied: Admin access or ownership required"
                )

            return func(*args, **kwargs)

        return wrapper

    return decorator


def manager_or_owner_required(obj_param: str = "obj") -> Callable:
    """Decorator that requires manager access or ownership."""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Find request object
            request = None
            for arg in args:
                if hasattr(arg, "user") and hasattr(arg, "META"):
                    request = arg
                    break
                if hasattr(arg, "request"):
                    request = arg.request
                    break

            if not request or not request.user or not request.user.is_authenticated:
                raise AuthenticationError("Authentication required")

            # Check if user is manager or admin
            if request.user.is_manager():
                return func(*args, **kwargs)

            # Check ownership
            obj = kwargs.get(obj_param)
            if not obj:
                raise APIPermissionError("Object not found")

            permission = IsOwnerOrManager()
            if not permission.has_object_permission(request, None, obj):
                raise APIPermissionError(
                    "Access denied: Manager access or ownership required"
                )

            return func(*args, **kwargs)

        return wrapper

    return decorator
