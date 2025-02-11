from django.db import models
from core.models import AbstractBaseModel
from .product import Product
from .product_variant import ProductVariant
from .choices import PriceAction


class ProductPriceHistory(AbstractBaseModel):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="price_history"
    )
    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE,
        related_name="price_history",
        null=True,
        blank=True,
    )
    action = models.CharField(max_length=50, choices=PriceAction.choices)
    previous_price = models.DecimalField(max_digits=10, decimal_places=2)
    new_price = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.CharField(max_length=255, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Product Price History"
        verbose_name_plural = "Product Price Histories"
        ordering = ["-created_at"]
