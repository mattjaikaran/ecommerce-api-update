from django.contrib import admin
from unfold.admin import ModelAdmin

from ..models import Product


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = (
        "name",
        "category",
        "price",
        "quantity",
        "status",
        "id",
        "is_active",
        "created_at",
    )
    list_filter = (
        "status",
        "is_active",
        "category",
        "type",
        "featured",
        "created_at",
    )
    search_fields = ("name", "description", "sku")
    readonly_fields = ("id", "created_at", "updated_at")
    ordering = ("-created_at",)
    fieldsets = (
        (
            "Basic Information",
            {"fields": ("name", "slug", "description", "category", "type")},
        ),
        (
            "Pricing & Inventory",
            {
                "fields": (
                    "price",
                    "compare_at_price",
                    "cost_price",
                    "quantity",
                    "low_stock_threshold",
                )
            },
        ),
        ("Classification", {"fields": ("tax_class", "shipping_class")}),
        (
            "Physical Properties",
            {
                "fields": ("weight", "length", "width", "height"),
                "classes": ("collapse",),
            },
        ),
        (
            "Digital Product",
            {"fields": ("digital_file", "download_limit"), "classes": ("collapse",)},
        ),
        ("Status & Visibility", {"fields": ("status", "is_active", "featured")}),
        (
            "SEO",
            {
                "fields": ("seo_title", "seo_description", "seo_keywords"),
                "classes": ("collapse",),
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
