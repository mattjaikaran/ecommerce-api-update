from django.contrib import admin
from unfold.admin import ModelAdmin

from ..models import BundleItem, ProductBundle


@admin.register(ProductBundle)
class ProductBundleAdmin(ModelAdmin):
    list_display = (
        "name",
        "discount_percentage",
        "is_active",
        "start_date",
        "end_date",
        "id",
        "created_at",
    )
    list_filter = ("is_active", "created_at")
    search_fields = ("name", "description")
    readonly_fields = ("id", "created_at", "updated_at")
    ordering = ("-created_at",)
    fieldsets = (
        ("Basic Information", {"fields": ("name", "slug", "description")}),
        ("Pricing", {"fields": ("discount_percentage",)}),
        ("Availability", {"fields": ("is_active", "start_date", "end_date")}),
        (
            "Metadata",
            {
                "fields": ("id", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(BundleItem)
class BundleItemAdmin(ModelAdmin):
    list_display = ("id", "bundle", "product", "quantity", "position", "created_at")
    list_filter = ("bundle", "created_at")
    search_fields = ("bundle__name", "product__name")
    readonly_fields = ("id", "created_at", "updated_at")
    ordering = ("bundle", "position")
    fieldsets = (
        (
            "Basic Information",
            {"fields": ("bundle", "product", "quantity", "position")},
        ),
        (
            "Metadata",
            {
                "fields": ("id", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )
