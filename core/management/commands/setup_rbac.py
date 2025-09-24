"""Management command to setup RBAC system with predefined roles and permissions."""

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from core.models import PermissionGroups, PredefinedRoles, Role


class Command(BaseCommand):
    """Setup RBAC system with predefined roles and permissions."""

    help = "Setup RBAC system with predefined roles and permissions"

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Force recreation of roles even if they exist",
        )
        parser.add_argument(
            "--roles",
            nargs="+",
            help="Specific roles to create (default: all)",
            choices=list(PredefinedRoles.ROLE_DEFINITIONS.keys()),
        )

    def handle(self, *args, **options):
        """Execute the command."""
        try:
            with transaction.atomic():
                self._setup_permissions()
                self._setup_roles(options)
                self.stdout.write(self.style.SUCCESS("Successfully setup RBAC system"))
        except Exception as e:
            raise CommandError(f"Failed to setup RBAC system: {e!s}")

    def _setup_permissions(self):
        """Ensure all required permissions exist."""
        self.stdout.write("Setting up permissions...")

        # Create custom permissions that might not exist
        custom_permissions = [
            ("core", "view_reports", "Can view reports"),
            ("core", "change_settings", "Can change system settings"),
            ("core", "manage_cache", "Can manage cache"),
            ("core", "view_logs", "Can view system logs"),
            ("orders", "process_order", "Can process orders"),
            ("orders", "cancel_order", "Can cancel orders"),
            ("orders", "refund_order", "Can refund orders"),
            ("orders", "view_order_reports", "Can view order reports"),
            ("orders", "change_order_status", "Can change order status"),
            ("products", "adjust_stock", "Can adjust product stock"),
            ("products", "view_stock_reports", "Can view stock reports"),
            ("products", "view_product_reports", "Can view product reports"),
            ("payments", "process_refund", "Can process payment refunds"),
            ("payments", "view_transactions", "Can view payment transactions"),
            ("payments", "view_payment_reports", "Can view payment reports"),
        ]

        created_count = 0
        for app_label, codename, name in custom_permissions:
            try:
                content_type = ContentType.objects.get(app_label=app_label)
                permission, created = Permission.objects.get_or_create(
                    codename=codename,
                    content_type=content_type,
                    defaults={"name": name},
                )
                if created:
                    created_count += 1
                    self.stdout.write(f"  Created permission: {app_label}.{codename}")
            except ContentType.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(
                        f"  Skipped permission {app_label}.{codename} - "
                        f"ContentType {app_label} does not exist"
                    )
                )

        self.stdout.write(f"Created {created_count} new permissions")

    def _setup_roles(self, options):
        """Setup predefined roles."""
        self.stdout.write("Setting up roles...")

        force = options.get("force", False)
        specific_roles = options.get("roles")

        roles_to_create = specific_roles or list(
            PredefinedRoles.ROLE_DEFINITIONS.keys()
        )

        for role_name in roles_to_create:
            if role_name not in PredefinedRoles.ROLE_DEFINITIONS:
                self.stdout.write(self.style.WARNING(f"  Unknown role: {role_name}"))
                continue

            role_def = PredefinedRoles.ROLE_DEFINITIONS[role_name]

            # Create or get role
            role, created = Role.objects.get_or_create(
                name=role_name,
                defaults={
                    "display_name": role_def["display_name"],
                    "description": role_def["description"],
                    "is_active": True,
                },
            )

            if created:
                self.stdout.write(f"  Created role: {role.display_name}")
            elif force:
                role.display_name = role_def["display_name"]
                role.description = role_def["description"]
                role.is_active = True
                role.save()
                self.stdout.write(f"  Updated role: {role.display_name}")
            else:
                self.stdout.write(f"  Role already exists: {role.display_name}")

            # Assign permissions to role
            self._assign_role_permissions(role, role_name, force)

    def _assign_role_permissions(self, role, role_name, force=False):
        """Assign permissions to a role based on predefined mappings."""
        # Clear existing permissions if forcing update
        if force:
            role.permissions.clear()

        # Get permissions for this role
        permissions_to_assign = self._get_role_permissions(role_name)

        assigned_count = 0
        for perm_codename in permissions_to_assign:
            try:
                # Parse app_label.codename format
                if "." in perm_codename:
                    app_label, codename = perm_codename.split(".", 1)
                else:
                    # Assume core app if no app specified
                    app_label, codename = "core", perm_codename

                content_type = ContentType.objects.get(app_label=app_label)
                permission = Permission.objects.get(
                    codename=codename, content_type=content_type
                )

                if not role.has_permission(permission) or force:
                    role.add_permission(permission)
                    assigned_count += 1

            except (Permission.DoesNotExist, ContentType.DoesNotExist):
                self.stdout.write(
                    self.style.WARNING(f"    Permission not found: {perm_codename}")
                )

        if assigned_count > 0:
            self.stdout.write(f"    Assigned {assigned_count} permissions")

    def _get_role_permissions(self, role_name):
        """Get permissions for a specific role."""
        # Map roles to permission groups
        role_permission_mapping = {
            PredefinedRoles.SUPERUSER: (
                PermissionGroups.USER_MANAGEMENT
                + PermissionGroups.PRODUCT_MANAGEMENT
                + PermissionGroups.ORDER_MANAGEMENT
                + PermissionGroups.INVENTORY_MANAGEMENT
                + PermissionGroups.PAYMENT_MANAGEMENT
                + PermissionGroups.REPORTING
                + PermissionGroups.SYSTEM_SETTINGS
                + PermissionGroups.CUSTOMER_SUPPORT
            ),
            PredefinedRoles.ADMIN: (
                PermissionGroups.USER_MANAGEMENT
                + PermissionGroups.PRODUCT_MANAGEMENT
                + PermissionGroups.ORDER_MANAGEMENT
                + PermissionGroups.INVENTORY_MANAGEMENT
                + PermissionGroups.PAYMENT_MANAGEMENT
                + PermissionGroups.REPORTING
                + PermissionGroups.SYSTEM_SETTINGS
                + PermissionGroups.CUSTOMER_SUPPORT
            ),
            PredefinedRoles.MANAGER: (
                PermissionGroups.ORDER_MANAGEMENT
                + PermissionGroups.INVENTORY_MANAGEMENT
                + PermissionGroups.PAYMENT_MANAGEMENT
                + PermissionGroups.REPORTING
                + PermissionGroups.CUSTOMER_SUPPORT
                + ["core.view_user", "products.view_product"]
            ),
            PredefinedRoles.STAFF: (
                PermissionGroups.ORDER_MANAGEMENT
                + PermissionGroups.CUSTOMER_SUPPORT
                + ["products.view_product", "core.view_customer"]
            ),
            PredefinedRoles.CUSTOMER: [
                "orders.view_order",
                "cart.add_cartitem",
                "cart.change_cartitem",
                "cart.delete_cartitem",
                "cart.view_cartitem",
                "core.view_customer_feedback",
                "core.add_customer_feedback",
            ],
            PredefinedRoles.VENDOR: (
                PermissionGroups.PRODUCT_MANAGEMENT
                + PermissionGroups.INVENTORY_MANAGEMENT
                + ["orders.view_order", "core.view_customer"]
            ),
            PredefinedRoles.SUPPORT: (
                PermissionGroups.CUSTOMER_SUPPORT
                + [
                    "orders.view_order",
                    "orders.change_order_status",
                    "core.view_customer",
                ]
            ),
        }

        return role_permission_mapping.get(role_name, [])
