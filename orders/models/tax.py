from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from core.models import AbstractBaseModel
from .order import Order
from .choices import TaxType


class Tax(AbstractBaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="taxes")
    tax_type = models.CharField(
        max_length=50, choices=TaxType.choices, default=TaxType.SALES
    )
    name = models.CharField(max_length=100)
    rate = models.DecimalField(
        max_digits=6,
        decimal_places=4,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
    )
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    jurisdiction = models.CharField(max_length=100, blank=True, null=True)
    meta_data = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"{self.name} for Order {self.order.order_number}"

    class Meta:
        verbose_name = "Tax"
        verbose_name_plural = "Taxes"
        ordering = ["id"]
        indexes = [
            models.Index(fields=["order", "tax_type"]),
        ]


class OrderTax(AbstractBaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    tax = models.ForeignKey(Tax, on_delete=models.CASCADE)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Tax for Order {self.order.order_number}"

    class Meta:
        verbose_name = "Order Tax"
        verbose_name_plural = "Order Taxes"
