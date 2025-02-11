from django.db import models
from django.contrib.auth import get_user_model
from core.models import AbstractBaseModel
from .order import Order
from .choices import OrderStatus

User = get_user_model()


class OrderHistory(AbstractBaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="history")
    status = models.CharField(max_length=50, choices=OrderStatus.choices)
    old_status = models.CharField(
        max_length=50, choices=OrderStatus.choices, null=True, blank=True
    )
    notes = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="order_status_changes"
    )
    meta_data = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"History for Order {self.order.order_number}"

    class Meta:
        verbose_name = "Order History"
        verbose_name_plural = "Order Histories"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["order", "status"]),
        ]
