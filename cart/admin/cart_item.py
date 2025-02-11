from django.contrib import admin
from unfold.admin import ModelAdmin
from ..models import CartItem


@admin.register(CartItem)
class CartItemAdmin(ModelAdmin):
    list_display = (
        "id",
        "cart",
        "product_variant",
        "quantity",
        "price",
        "created_at",
    )
    list_filter = ("cart__is_active", "created_at")
    search_fields = (
        "cart__customer__email",
        "product_variant__product__name",
        "product_variant__sku",
    )
    readonly_fields = ("id", "created_at", "updated_at")
    ordering = ("-created_at",)
    fieldsets = (
        ("Basic Information", {"fields": ("cart", "product_variant")}),
        ("Quantity & Price", {"fields": ("quantity", "price")}),
        (
            "Metadata",
            {"fields": ("id", "created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )
