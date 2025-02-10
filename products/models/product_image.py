from django.db import models
from core.models import AbstractBaseModel
from .product import Product
from .product_variant import ProductVariant


class ProductImage(AbstractBaseModel):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE,
        related_name="images",
        null=True,
        blank=True,
    )
    image = models.ImageField(upload_to="products/images/")
    alt_text = models.CharField(max_length=255, null=True, blank=True)
    position = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"
        ordering = ["position"]
