from django.db import models
from core.models import AbstractBaseModel
from .order import Order


class OrderDiscount(AbstractBaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Discount for Order {self.order.order_number}"

    class Meta:
        verbose_name = "Order Discount"
        verbose_name_plural = "Order Discounts"
