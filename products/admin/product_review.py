from django.contrib import admin
from unfold.admin import ModelAdmin
from ..models import ProductReview


@admin.register(ProductReview)
class ProductReviewAdmin(ModelAdmin):
    list_display = (
        "id",
        "product",
        "user",
        "rating",
        "title",
        "is_verified",
        "is_featured",
        "created_at",
    )
    list_filter = ("rating", "is_verified", "is_featured", "created_at")
    search_fields = ("product__name", "user__username", "title", "comment")
    readonly_fields = ("id", "created_at", "updated_at")
    ordering = ("-created_at",)
    fieldsets = (
        (
            "Review Information",
            {"fields": ("product", "user", "rating", "title", "comment")},
        ),
        ("Status", {"fields": ("is_verified", "is_featured")}),
        (
            "Metadata",
            {
                "fields": ("id", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )
