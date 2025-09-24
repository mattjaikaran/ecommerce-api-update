from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from core.models import AbstractBaseModel
from products.models import ProductVariant

from .order import Order


class OrderLineItem(AbstractBaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product_variant = models.ForeignKey(
        ProductVariant, on_delete=models.PROTECT, related_name="order_items"
    )
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    subtotal = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    discount_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, validators=[MinValueValidator(0)]
    )
    tax_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, validators=[MinValueValidator(0)]
    )
    total = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    tax_rate = models.DecimalField(
        max_digits=6,
        decimal_places=4,
        default=0.00,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
    )
    weight = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, validators=[MinValueValidator(0)]
    )
    meta_data = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"Order {self.order.order_number} - {self.product_variant.name}"

    class Meta:
        verbose_name = "Order Line Item"
        verbose_name_plural = "Order Line Items"
        ordering = ["id"]
        indexes = [
            models.Index(fields=["order", "product_variant"]),
        ]
