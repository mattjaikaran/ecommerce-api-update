from django.contrib import admin
from unfold.admin import ModelAdmin
from ..models import OrderLineItem


@admin.register(OrderLineItem)
class OrderLineItemAdmin(ModelAdmin):
    list_display = (
        "id",
        "order",
        "product_variant",
        "quantity",
        "unit_price",
        "total",
        "created_at",
    )
    list_filter = ("order__status", "created_at")
    search_fields = (
        "order__order_number",
        "product_variant__name",
        "product_variant__sku",
    )
    readonly_fields = ("id", "created_at", "updated_at")
    ordering = ("-created_at",)
    fieldsets = (
        ("Basic Information", {"fields": ("order", "product_variant", "quantity")}),
        (
            "Pricing",
            {
                "fields": (
                    "unit_price",
                    "subtotal",
                    "discount_amount",
                    "tax_amount",
                    "total",
                    "tax_rate",
                )
            },
        ),
        ("Physical", {"fields": ("weight",)}),
        (
            "Metadata",
            {
                "fields": ("id", "meta_data", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )
