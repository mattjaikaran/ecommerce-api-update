from django.contrib import admin
from unfold.admin import ModelAdmin

from ..models import Refund


@admin.register(Refund)
class RefundAdmin(ModelAdmin):
    list_display = (
        "id",
        "order",
        "transaction",
        "amount",
        "status",
        "refund_transaction_id",
        "created_at",
    )
    list_filter = ("status", "created_at")
    search_fields = (
        "order__order_number",
        "transaction__transaction_id",
        "refund_transaction_id",
        "reason",
    )
    readonly_fields = ("id", "created_at", "updated_at")
    ordering = ("-created_at",)
    fieldsets = (
        ("Basic Information", {"fields": ("order", "transaction", "amount", "status")}),
        (
            "Refund Details",
            {
                "fields": (
                    "reason",
                    "notes",
                    "refund_transaction_id",
                    "gateway_response",
                )
            },
        ),
        (
            "Metadata",
            {
                "fields": ("id", "meta_data", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )
