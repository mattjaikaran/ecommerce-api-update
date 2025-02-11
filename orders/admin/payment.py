from django.contrib import admin
from unfold.admin import ModelAdmin
from ..models import PaymentTransaction, OrderPayment


@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(ModelAdmin):
    list_display = (
        "id",
        "order",
        "transaction_id",
        "payment_method",
        "amount",
        "status",
        "created_at",
    )
    list_filter = ("status", "payment_method", "gateway", "created_at")
    search_fields = ("order__order_number", "transaction_id", "gateway_response")
    readonly_fields = ("id", "created_at", "updated_at")
    ordering = ("-created_at",)
    fieldsets = (
        (
            "Basic Information",
            {"fields": ("order", "transaction_id", "payment_method")},
        ),
        ("Payment Details", {"fields": ("amount", "currency", "status")}),
        (
            "Gateway Information",
            {"fields": ("gateway", "gateway_response", "error_message")},
        ),
        (
            "Metadata",
            {
                "fields": ("id", "meta_data", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(OrderPayment)
class OrderPaymentAdmin(ModelAdmin):
    list_display = ("id", "order", "amount", "created_at")
    list_filter = ("created_at",)
    search_fields = ("order__order_number",)
    readonly_fields = ("id", "created_at", "updated_at")
    ordering = ("-created_at",)
    fieldsets = (
        ("Basic Information", {"fields": ("order", "amount", "notes")}),
        (
            "Metadata",
            {
                "fields": ("id", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )
