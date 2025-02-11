from django.contrib import admin
from unfold.admin import ModelAdmin
from ..models import (
    FulfillmentOrder,
    FulfillmentLineItem,
    OrderFulfillment,
    OrderFulfillmentItem,
    OrderFulfillmentTracking,
    OrderFulfillmentTrackingUrl,
)


@admin.register(FulfillmentOrder)
class FulfillmentOrderAdmin(ModelAdmin):
    list_display = (
        "id",
        "order",
        "status",
        "shipping_method",
        "tracking_number",
        "created_at",
    )
    list_filter = ("status", "shipping_method", "created_at")
    search_fields = ("order__order_number", "tracking_number", "shipping_carrier")
    readonly_fields = ("id", "created_at", "updated_at")
    ordering = ("-created_at",)
    fieldsets = (
        ("Basic Information", {"fields": ("order", "status", "shipping_method")}),
        (
            "Tracking",
            {
                "fields": (
                    "tracking_number",
                    "tracking_url",
                    "shipping_carrier",
                    "shipping_label_url",
                )
            },
        ),
        ("Notes", {"fields": ("notes",)}),
        (
            "Metadata",
            {
                "fields": ("id", "meta_data", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(FulfillmentLineItem)
class FulfillmentLineItemAdmin(ModelAdmin):
    list_display = ("id", "fulfillment", "order_item", "quantity", "created_at")
    list_filter = ("fulfillment__status", "created_at")
    search_fields = (
        "fulfillment__order__order_number",
        "order_item__product_variant__name",
    )
    readonly_fields = ("id", "created_at", "updated_at")
    ordering = ("-created_at",)
    fieldsets = (
        ("Basic Information", {"fields": ("fulfillment", "order_item", "quantity")}),
        (
            "Metadata",
            {
                "fields": ("id", "meta_data", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(OrderFulfillment)
class OrderFulfillmentAdmin(ModelAdmin):
    list_display = ("id", "order", "fulfillment_order", "created_at")
    list_filter = ("created_at",)
    search_fields = ("order__order_number",)
    readonly_fields = ("id", "created_at", "updated_at")
    ordering = ("-created_at",)
    fieldsets = (
        ("Basic Information", {"fields": ("order", "fulfillment_order", "notes")}),
        (
            "Metadata",
            {
                "fields": ("id", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(OrderFulfillmentItem)
class OrderFulfillmentItemAdmin(ModelAdmin):
    list_display = ("id", "fulfillment_order", "order_line_item", "created_at")
    list_filter = ("created_at",)
    search_fields = ("fulfillment_order__order__order_number",)
    readonly_fields = ("id", "created_at", "updated_at")
    ordering = ("-created_at",)
    fieldsets = (
        (
            "Basic Information",
            {"fields": ("fulfillment_order", "order_line_item", "notes")},
        ),
        (
            "Metadata",
            {
                "fields": ("id", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(OrderFulfillmentTracking)
class OrderFulfillmentTrackingAdmin(ModelAdmin):
    list_display = ("id", "fulfillment_order", "tracking_number", "created_at")
    list_filter = ("created_at",)
    search_fields = ("fulfillment_order__order__order_number", "tracking_number")
    readonly_fields = ("id", "created_at", "updated_at")
    ordering = ("-created_at",)
    fieldsets = (
        (
            "Basic Information",
            {"fields": ("fulfillment_order", "tracking_number", "notes")},
        ),
        (
            "Metadata",
            {
                "fields": ("id", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(OrderFulfillmentTrackingUrl)
class OrderFulfillmentTrackingUrlAdmin(ModelAdmin):
    list_display = ("id", "fulfillment_tracking", "url", "created_at")
    list_filter = ("created_at",)
    search_fields = ("fulfillment_tracking__tracking_number", "url")
    readonly_fields = ("id", "created_at", "updated_at")
    ordering = ("-created_at",)
    fieldsets = (
        ("Basic Information", {"fields": ("fulfillment_tracking", "url", "notes")}),
        (
            "Metadata",
            {
                "fields": ("id", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )
