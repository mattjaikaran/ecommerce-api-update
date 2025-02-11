from django.contrib import admin
from unfold.admin import ModelAdmin
from ..models import OrderNote


@admin.register(OrderNote)
class OrderNoteAdmin(ModelAdmin):
    list_display = (
        "id",
        "order",
        "note",
        "is_customer_visible",
        "created_by",
        "created_at",
    )
    list_filter = ("is_customer_visible", "created_at")
    search_fields = ("order__order_number", "note", "created_by__email")
    readonly_fields = ("id", "created_at", "updated_at")
    ordering = ("-created_at",)
    fieldsets = (
        (
            "Basic Information",
            {"fields": ("order", "note", "is_customer_visible", "created_by")},
        ),
        (
            "Metadata",
            {
                "fields": ("id", "meta_data", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )
