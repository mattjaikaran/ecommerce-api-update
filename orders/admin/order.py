from django.contrib import admin
from unfold.admin import ModelAdmin
from ..models import Order


@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = (
        "id",
        "order_number",
        "customer",
        "status",
        "payment_status",
        "total",
        "created_at",
    )
    list_filter = (
        "status",
        "payment_status",
        "payment_method",
        "shipping_method",
        "created_at",
    )
    search_fields = (
        "order_number",
        "customer__email",
        "email",
        "phone",
        "billing_address__address1",
        "shipping_address__address1",
    )
    readonly_fields = ("id", "order_number", "created_at", "updated_at")
    ordering = ("-created_at",)
    fieldsets = (
        (
            "Order Information",
            {"fields": ("order_number", "customer", "customer_group", "status")},
        ),
        (
            "Financial",
            {
                "fields": (
                    "currency",
                    "subtotal",
                    "shipping_amount",
                    "shipping_tax_amount",
                    "discount_amount",
                    "tax_amount",
                    "total",
                )
            },
        ),
        (
            "Payment",
            {
                "fields": (
                    "payment_status",
                    "payment_method",
                    "payment_gateway",
                    "payment_gateway_id",
                    "payment_gateway_response",
                )
            },
        ),
        (
            "Shipping",
            {"fields": ("shipping_method", "billing_address", "shipping_address")},
        ),
        ("Contact", {"fields": ("email", "phone")}),
        ("Notes", {"fields": ("customer_note", "staff_notes")}),
        (
            "Technical",
            {"fields": ("ip_address", "user_agent"), "classes": ("collapse",)},
        ),
        (
            "Metadata",
            {
                "fields": ("id", "meta_data", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )
