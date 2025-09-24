from django.db import models

from core.models import AbstractBaseModel

from .choices import RelatedProductType
from .product import Product


class RelatedProduct(AbstractBaseModel):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="related_products"
    )
    related_product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="related_to_products"
    )
    relationship_type = models.CharField(
        max_length=50, choices=RelatedProductType.choices
    )
    position = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.product.name} -> {self.related_product.name} ({self.get_relationship_type_display()})"

    class Meta:
        verbose_name = "Related Product"
        verbose_name_plural = "Related Products"
        ordering = ["position"]
        unique_together = ["product", "related_product", "relationship_type"]
