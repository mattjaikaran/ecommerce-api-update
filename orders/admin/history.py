from django.contrib import admin
from unfold.admin import ModelAdmin
from ..models import OrderHistory


@admin.register(OrderHistory)
class OrderHistoryAdmin(ModelAdmin):
    list_display = ("id", "order", "status", "old_status", "created_by", "created_at")
    list_filter = ("status", "old_status", "created_at")
    search_fields = ("order__order_number", "notes", "created_by__email")
    readonly_fields = ("id", "created_at", "updated_at")
    ordering = ("-created_at",)
    fieldsets = (
        (
            "Basic Information",
            {"fields": ("order", "status", "old_status", "created_by")},
        ),
        ("Notes", {"fields": ("notes",)}),
        (
            "Metadata",
            {
                "fields": ("id", "meta_data", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )
