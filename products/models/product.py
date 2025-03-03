from django.db import models
import uuid
from core.models import AbstractBaseModel
from .choices import ProductStatus, ProductType, TaxClass, ShippingClass
from .product_category import ProductCategory


class Product(AbstractBaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(
        ProductCategory, on_delete=models.CASCADE, related_name="products"
    )
    type = models.CharField(
        max_length=50, choices=ProductType.choices, default=ProductType.PHYSICAL
    )
    tax_class = models.CharField(
        max_length=50, choices=TaxClass.choices, default=TaxClass.STANDARD
    )
    shipping_class = models.CharField(
        max_length=50, choices=ShippingClass.choices, default=ShippingClass.STANDARD
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    compare_at_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    cost_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    quantity = models.IntegerField(default=0)
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
    digital_file = models.FileField(
        upload_to="products/digital/",
        null=True,
        blank=True,
        help_text="Upload digital product file",
    )
    download_limit = models.IntegerField(
        null=True,
        blank=True,
        help_text="Number of times digital product can be downloaded",
    )
    is_active = models.BooleanField(default=True)
    status = models.CharField(
        max_length=50, choices=ProductStatus.choices, default=ProductStatus.DRAFT
    )
    featured = models.BooleanField(default=False)
    seo_title = models.CharField(max_length=255, null=True, blank=True)
    seo_description = models.TextField(null=True, blank=True)
    seo_keywords = models.TextField(null=True, blank=True)
    meta_data = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ["-created_at"]
