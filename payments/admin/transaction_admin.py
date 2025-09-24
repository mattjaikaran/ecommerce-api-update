from django.contrib import admin
from unfold.admin import ModelAdmin

from ..models import Transaction


@admin.register(Transaction)
class TransactionAdmin(ModelAdmin):
    list_display = (
        "id",
        "order",
        "payment_method",
        "transaction_id",
        "transaction_type",
        "transaction_status",
        "transaction_amount",
        "transaction_currency",
        "created_at",
    )
    list_filter = (
        "transaction_status",
        "transaction_type",
        "payment_method",
        "transaction_currency",
        "created_at",
    )
    search_fields = ("order__order_number", "transaction_id", "notes")
    readonly_fields = ("id", "created_at", "updated_at")
    ordering = ("-created_at",)
    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "order",
                    "payment_method",
                    "transaction_id",
                    "transaction_type",
                    "transaction_status",
                )
            },
        ),
        (
            "Amount Details",
            {
                "fields": (
                    "transaction_amount",
                    "transaction_currency",
                    "transaction_fee",
                    "transaction_tax",
                    "transaction_total",
                )
            },
        ),
        ("Response", {"fields": ("transaction_response",), "classes": ("collapse",)}),
        ("Notes", {"fields": ("notes",)}),
        (
            "Metadata",
            {"fields": ("id", "created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )
