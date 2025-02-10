from django.db import models
from django.core.validators import MinValueValidator
from core.models import AbstractBaseModel
from .order import Order
from .order_line_item import OrderLineItem
from .choices import FulfillmentStatus, ShippingMethod


class FulfillmentOrder(AbstractBaseModel):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="fulfillments"
    )
    status = models.CharField(
        max_length=50,
        choices=FulfillmentStatus.choices,
        default=FulfillmentStatus.PENDING,
    )
    tracking_number = models.CharField(max_length=255, blank=True, null=True)
    tracking_url = models.URLField(blank=True, null=True)
    shipping_carrier = models.CharField(max_length=100, blank=True, null=True)
    shipping_method = models.CharField(
        max_length=50, choices=ShippingMethod.choices, default=ShippingMethod.STANDARD
    )
    shipping_label_url = models.URLField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    meta_data = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"Fulfillment {self.id} for Order {self.order.order_number}"

    class Meta:
        verbose_name = "Fulfillment Order"
        verbose_name_plural = "Fulfillment Orders"
        ordering = ["-date_created"]
        indexes = [
            models.Index(fields=["order", "status"]),
            models.Index(fields=["tracking_number"]),
        ]


class FulfillmentLineItem(AbstractBaseModel):
    fulfillment = models.ForeignKey(
        FulfillmentOrder, on_delete=models.CASCADE, related_name="items"
    )
    order_item = models.ForeignKey(
        OrderLineItem, on_delete=models.CASCADE, related_name="fulfillment_items"
    )
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    meta_data = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"Fulfillment Item {self.id} for Order {self.fulfillment.order.order_number}"

    class Meta:
        verbose_name = "Fulfillment Line Item"
        verbose_name_plural = "Fulfillment Line Items"
        ordering = ["id"]
        indexes = [
            models.Index(fields=["fulfillment", "order_item"]),
        ]


class OrderFulfillment(AbstractBaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    fulfillment_order = models.ForeignKey(FulfillmentOrder, on_delete=models.CASCADE)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Fulfillment for Order {self.order.order_number}"

    class Meta:
        verbose_name = "Order Fulfillment"
        verbose_name_plural = "Order Fulfillments"


class OrderFulfillmentItem(AbstractBaseModel):
    fulfillment_order = models.ForeignKey(FulfillmentOrder, on_delete=models.CASCADE)
    order_line_item = models.ForeignKey(OrderLineItem, on_delete=models.CASCADE)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Fulfillment Item for Order {self.fulfillment_order.order.order_number}"

    class Meta:
        verbose_name = "Order Fulfillment Item"
        verbose_name_plural = "Order Fulfillment Items"


class OrderFulfillmentTracking(AbstractBaseModel):
    fulfillment_order = models.ForeignKey(FulfillmentOrder, on_delete=models.CASCADE)
    tracking_number = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Tracking for Order {self.fulfillment_order.order.order_number}"

    class Meta:
        verbose_name = "Order Fulfillment Tracking"
        verbose_name_plural = "Order Fulfillment Trackings"


class OrderFulfillmentTrackingUrl(AbstractBaseModel):
    fulfillment_tracking = models.ForeignKey(
        OrderFulfillmentTracking, on_delete=models.CASCADE
    )
    url = models.URLField()
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Tracking URL for Order {self.fulfillment_tracking.fulfillment_order.order.order_number}"

    class Meta:
        verbose_name = "Order Fulfillment Tracking URL"
        verbose_name_plural = "Order Fulfillment Tracking URLs"
