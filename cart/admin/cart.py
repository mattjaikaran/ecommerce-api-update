from django.contrib import admin
from unfold.admin import ModelAdmin
from ..models import Cart


@admin.register(Cart)
class CartAdmin(ModelAdmin):
    list_display = (
        "id",
        "customer",
        "session_key",
        "subtotal",
        "total_price",
        "total_quantity",
        "is_active",
        "expires_at",
        "created_at",
    )
    list_filter = ("is_active", "created_at", "expires_at")
    search_fields = ("customer__email", "session_key")
    readonly_fields = ("id", "created_at", "updated_at")
    ordering = ("-created_at",)
    fieldsets = (
        (
            "Basic Information",
            {"fields": ("customer", "session_key", "is_active")},
        ),
        ("Totals", {"fields": ("subtotal", "total_price", "total_quantity")}),
        ("Expiration", {"fields": ("expires_at",)}),
        (
            "Metadata",
            {"fields": ("id", "created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )
