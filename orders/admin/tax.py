from django.contrib import admin
from unfold.admin import ModelAdmin
from ..models import Tax, OrderTax


@admin.register(Tax)
class TaxAdmin(ModelAdmin):
    list_display = (
        "id",
        "order",
        "tax_type",
        "name",
        "rate",
        "amount",
        "jurisdiction",
        "created_at",
    )
    list_filter = ("tax_type", "created_at")
    search_fields = ("order__order_number", "name", "jurisdiction")
    readonly_fields = ("id", "created_at", "updated_at")
    ordering = ("-created_at",)
    fieldsets = (
        ("Basic Information", {"fields": ("order", "tax_type", "name")}),
        ("Tax Details", {"fields": ("rate", "amount", "jurisdiction")}),
        (
            "Metadata",
            {
                "fields": ("id", "meta_data", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(OrderTax)
class OrderTaxAdmin(ModelAdmin):
    list_display = ("id", "order", "tax", "created_at")
    list_filter = ("created_at",)
    search_fields = ("order__order_number", "tax__name")
    readonly_fields = ("id", "created_at", "updated_at")
    ordering = ("-created_at",)
    fieldsets = (
        ("Basic Information", {"fields": ("order", "tax", "notes")}),
        (
            "Metadata",
            {
                "fields": ("id", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )
