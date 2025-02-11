from django.contrib import admin
from unfold.admin import ModelAdmin
from ..models import Refund


@admin.register(Refund)
class RefundAdmin(ModelAdmin):
    list_display = ("id", "transaction", "amount", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = (
        "transaction__order__order_number",
        "transaction__transaction_id",
        "notes",
    )
    readonly_fields = ("id", "created_at", "updated_at")
    ordering = ("-created_at",)
    fieldsets = (
        ("Basic Information", {"fields": ("transaction", "amount", "status")}),
        ("Notes", {"fields": ("notes",)}),
        (
            "Metadata",
            {"fields": ("id", "created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )
