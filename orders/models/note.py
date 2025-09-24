from django.contrib.auth import get_user_model
from django.db import models

from core.models import AbstractBaseModel

from .order import Order

User = get_user_model()


class OrderNote(AbstractBaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="notes")
    note = models.TextField()
    is_customer_visible = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="order_notes"
    )
    meta_data = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"Note for Order {self.order.order_number}"

    class Meta:
        verbose_name = "Order Note"
        verbose_name_plural = "Order Notes"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["order", "is_customer_visible"]),
        ]
