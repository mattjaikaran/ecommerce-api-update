from django.db import models
from core.models import AbstractBaseModel
from .product import Product
from .product_variant import ProductVariant
from .choices import InventoryAction


class ProductInventoryHistory(AbstractBaseModel):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="inventory_history"
    )
    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE,
        related_name="inventory_history",
        null=True,
        blank=True,
    )
    action = models.CharField(max_length=50, choices=InventoryAction.choices)
    quantity = models.IntegerField()
    previous_quantity = models.IntegerField()
    new_quantity = models.IntegerField()
    reference = models.CharField(
        max_length=255, null=True, blank=True
    )  # Order number, return number, etc.
    notes = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Product Inventory History"
        verbose_name_plural = "Product Inventory Histories"
        ordering = ["-created_at"]
