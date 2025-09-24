from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from core.models import AbstractBaseModel

from .product import Product


class ProductBundle(AbstractBaseModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    discount_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    is_active = models.BooleanField(default=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Product Bundle"
        verbose_name_plural = "Product Bundles"
        ordering = ["-created_at"]


class BundleItem(AbstractBaseModel):
    bundle = models.ForeignKey(
        ProductBundle, on_delete=models.CASCADE, related_name="items"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    position = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.bundle.name} - {self.product.name} (x{self.quantity})"

    class Meta:
        verbose_name = "Bundle Item"
        verbose_name_plural = "Bundle Items"
        ordering = ["position"]
        unique_together = ["bundle", "product"]
