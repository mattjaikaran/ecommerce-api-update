from django.contrib import admin
from unfold.admin import ModelAdmin
from ..models import ProductVariant


@admin.register(ProductVariant)
class ProductVariantAdmin(ModelAdmin):
    list_display = (
        "id",
        "product",
        "name",
        "sku",
        "price",
        "inventory_quantity",
        "is_active",
        "created_at",
    )
    list_filter = ("is_active", "product", "created_at")
    search_fields = ("name", "sku", "barcode")
    readonly_fields = ("id", "created_at", "updated_at")
    ordering = ("product", "position")
    fieldsets = (
        ("Basic Information", {"fields": ("product", "name", "sku", "barcode")}),
        ("Pricing", {"fields": ("price", "compare_at_price", "cost_price")}),
        ("Inventory", {"fields": ("inventory_quantity", "low_stock_threshold")}),
        (
            "Physical Properties",
            {
                "fields": ("weight", "length", "width", "height"),
                "classes": ("collapse",),
            },
        ),
        ("Display Settings", {"fields": ("position", "is_active")}),
        (
            "Metadata",
            {
                "fields": ("id", "meta_data", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )
