from django.contrib import admin
from unfold.admin import ModelAdmin

from ..models import ProductCategory


@admin.register(ProductCategory)
class ProductCategoryAdmin(ModelAdmin):
    list_display = ("name", "parent", "is_active", "id", "position", "created_at")
    list_filter = ("is_active", "parent", "created_at")
    search_fields = ("name", "description")
    readonly_fields = ("id", "created_at", "updated_at")
    ordering = ("position", "name")
    fieldsets = (
        (
            "Basic Information",
            {"fields": ("name", "slug", "description", "parent", "image")},
        ),
        ("Display Settings", {"fields": ("position", "is_active")}),
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
                "fields": ("id", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )
