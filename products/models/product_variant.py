from django.db import models

from core.models import AbstractBaseModel

from .product import Product


class ProductVariant(AbstractBaseModel):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="variants"
    )
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=255, unique=True)
    barcode = models.CharField(max_length=255, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    compare_at_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    cost_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    inventory_quantity = models.IntegerField(default=0)
    low_stock_threshold = models.IntegerField(default=10)
    weight = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Weight in kilograms",
    )
    length = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Length in centimeters",
    )
    width = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Width in centimeters",
    )
    height = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Height in centimeters",
    )
    position = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    meta_data = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"{self.product.name} - {self.name}"

    class Meta:
        verbose_name = "Product Variant"
        verbose_name_plural = "Product Variants"
        ordering = ["position"]
        unique_together = ["product", "sku"]
        indexes = [
            # Core lookup indexes
            models.Index(fields=["sku"]),
            models.Index(fields=["barcode"]),
            models.Index(fields=["product"]),
            models.Index(fields=["is_active"]),
            # Inventory and pricing indexes
            models.Index(fields=["inventory_quantity"]),
            models.Index(fields=["price"]),
            models.Index(fields=["position"]),
            # Compound indexes for common queries
            models.Index(fields=["product", "is_active"]),
            models.Index(fields=["product", "position"]),
            models.Index(fields=["is_active", "inventory_quantity"]),
            models.Index(fields=["product", "price"]),
            # Date-based indexes
            models.Index(fields=["created_at"]),
            models.Index(fields=["updated_at"]),
        ]
