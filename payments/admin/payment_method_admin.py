from django.contrib import admin
from unfold.admin import ModelAdmin

from ..models import PaymentMethod


@admin.register(PaymentMethod)
class PaymentMethodAdmin(ModelAdmin):
    list_display = (
        "id",
        "name",
        "code",
        "provider",
        "is_active",
        "position",
        "created_at",
    )
    list_filter = ("is_active", "provider", "created_at")
    search_fields = ("name", "code", "description")
    readonly_fields = ("id", "created_at", "updated_at")
    ordering = ("position", "name")
    fieldsets = (
        ("Basic Information", {"fields": ("name", "code", "description", "provider")}),
        ("Display Settings", {"fields": ("icon", "position", "is_active")}),
        (
            "Configuration",
            {"fields": ("config", "credentials"), "classes": ("collapse",)},
        ),
        (
            "Metadata",
            {"fields": ("id", "created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )
