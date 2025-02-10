from django.db import models
from core.models import AbstractBaseModel
from .product_variant import ProductVariant


class ProductOption(AbstractBaseModel):
    name = models.CharField(max_length=255)
    position = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Product Option"
        verbose_name_plural = "Product Options"
        ordering = ["position"]


class ProductOptionValue(AbstractBaseModel):
    option = models.ForeignKey(
        ProductOption, on_delete=models.CASCADE, related_name="values"
    )
    name = models.CharField(max_length=255)
    position = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.option.name} - {self.name}"

    class Meta:
        verbose_name = "Product Option Value"
        verbose_name_plural = "Product Option Values"
        ordering = ["position"]


class ProductVariantOption(AbstractBaseModel):
    variant = models.ForeignKey(
        ProductVariant, on_delete=models.CASCADE, related_name="options"
    )
    option = models.ForeignKey(ProductOption, on_delete=models.CASCADE)
    value = models.ForeignKey(ProductOptionValue, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.variant.name} - {self.option.name}: {self.value.name}"

    class Meta:
        verbose_name = "Product Variant Option"
        verbose_name_plural = "Product Variant Options"
        unique_together = ["variant", "option"]
