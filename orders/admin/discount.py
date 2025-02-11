from django.contrib import admin
from unfold.admin import ModelAdmin
from ..models import OrderDiscount


@admin.register(OrderDiscount)
class OrderDiscountAdmin(ModelAdmin):
    list_display = ("id", "order", "amount", "created_at")
    list_filter = ("created_at",)
    search_fields = ("order__order_number", "notes")
    readonly_fields = ("id", "created_at", "updated_at")
    ordering = ("-created_at",)
    fieldsets = (
        ("Basic Information", {"fields": ("order", "amount", "notes")}),
        (
            "Metadata",
            {
                "fields": ("id", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )
