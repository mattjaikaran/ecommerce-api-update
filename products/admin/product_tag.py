from django.contrib import admin
from unfold.admin import ModelAdmin
from ..models import ProductTag, ProductCollection


@admin.register(ProductTag)
class ProductTagAdmin(ModelAdmin):
    list_display = ("id", "name", "slug", "created_at")
    search_fields = ("name", "description")
    readonly_fields = ("id", "created_at", "updated_at")
    ordering = ("name",)
    fieldsets = (
        ("Basic Information", {"fields": ("name", "slug", "description")}),
        ("Products", {"fields": ("products",)}),
        (
            "Metadata",
            {
                "fields": ("id", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(ProductCollection)
class ProductCollectionAdmin(ModelAdmin):
    list_display = ("id", "name", "slug", "is_active", "position", "created_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("name", "description")
    readonly_fields = ("id", "created_at", "updated_at")
    ordering = ("position", "name")
    fieldsets = (
        ("Basic Information", {"fields": ("name", "slug", "description", "image")}),
        ("Display Settings", {"fields": ("position", "is_active")}),
        ("Products", {"fields": ("products",)}),
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
