from django.contrib import admin
from unfold.admin import ModelAdmin

from ..models import ProductAttribute, ProductAttributeAssignment, ProductAttributeValue


@admin.register(ProductAttribute)
class ProductAttributeAdmin(ModelAdmin):
    list_display = (
        "name",
        "code",
        "display_type",
        "is_filterable",
        "is_variation",
        "position",
        "id",
        "created_at",
    )
    list_filter = (
        "is_filterable",
        "is_searchable",
        "is_required",
        "is_visible",
        "is_variation",
        "display_type",
        "validation_type",
    )
    search_fields = ("name", "code", "description")
    readonly_fields = ("id", "created_at", "updated_at")
    ordering = ("position", "name")
    fieldsets = (
        ("Basic Information", {"fields": ("name", "code", "description", "position")}),
        ("Display Settings", {"fields": ("display_type", "icon", "help_text", "unit")}),
        (
            "Behavior",
            {
                "fields": (
                    "is_filterable",
                    "is_searchable",
                    "is_required",
                    "is_visible",
                    "is_variation",
                )
            },
        ),
        (
            "Validation",
            {
                "fields": (
                    "validation_type",
                    "validation_regex",
                    "validation_message",
                    "default_value",
                    "min_value",
                    "max_value",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Metadata",
            {
                "fields": ("id", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(ProductAttributeValue)
class ProductAttributeValueAdmin(ModelAdmin):
    list_display = (
        "id",
        "attribute",
        "value",
        "display_value",
        "position",
        "is_active",
        "created_at",
    )
    list_filter = ("attribute", "is_active", "is_default")
    search_fields = ("value", "display_value")
    readonly_fields = ("id", "created_at", "updated_at")
    ordering = ("attribute", "position")
    fieldsets = (
        (
            "Basic Information",
            {"fields": ("attribute", "value", "display_value", "position")},
        ),
        ("Display Settings", {"fields": ("color_code", "image", "icon", "tooltip")}),
        ("Status", {"fields": ("is_active", "is_default")}),
        (
            "Metadata",
            {
                "fields": ("id", "meta_data", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(ProductAttributeAssignment)
class ProductAttributeAssignmentAdmin(ModelAdmin):
    list_display = (
        "id",
        "product",
        "attribute",
        "value",
        "is_visible",
        "is_variation",
        "created_at",
    )
    list_filter = ("is_visible", "is_variation", "attribute")
    search_fields = ("product__name", "attribute__name", "value__value")
    readonly_fields = ("id", "created_at", "updated_at")
    ordering = ("product", "position")
    fieldsets = (
        (
            "Basic Information",
            {"fields": ("product", "attribute", "value", "position")},
        ),
        ("Display & Behavior", {"fields": ("is_visible", "is_variation")}),
        (
            "Adjustments",
            {
                "fields": ("price_adjustment", "weight_adjustment"),
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
