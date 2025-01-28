from django.db import models
import uuid
from core.models import AbstractBaseModel
from django.contrib.auth import get_user_model

User = get_user_model()


class ProductCategory(AbstractBaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, related_name="children", null=True, blank=True
    )
    seo_title = models.CharField(max_length=255, null=True, blank=True)
    seo_description = models.TextField(null=True, blank=True)
    seo_keywords = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Product Category"
        verbose_name_plural = "Product Categories"


class Product(AbstractBaseModel):
    """
    Model representing a products.

    This model includes a UUID primary key and a name field.
    Additional fields can be added as needed.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(
        ProductCategory, on_delete=models.CASCADE, related_name="products"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=0)
    image = models.ImageField(upload_to="products/images/", null=True, blank=True)
    is_active = models.BooleanField(default=True)
    status = models.CharField(
        max_length=255,
        choices=[("draft", "Draft"), ("active", "Active"), ("archived", "Archived")],
        default="draft",
    )
    seo_title = models.CharField(max_length=255, null=True, blank=True)
    seo_description = models.TextField(null=True, blank=True)
    seo_keywords = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"


class ProductVariant(AbstractBaseModel):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="variants"
    )
    sku = models.CharField(max_length=255)
    barcode = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    compare_at_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    inventory_quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.sku

    class Meta:
        verbose_name = "Product Variant"
        verbose_name_plural = "Product Variants"


class ProductOption(AbstractBaseModel):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="options"
    )
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.product.name} - {self.name}: {self.value}"

    class Meta:
        verbose_name = "Product Option"
        verbose_name_plural = "Product Options"


class ProductImage(AbstractBaseModel):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="products/images/", null=True, blank=True)
    alt_text = models.CharField(max_length=255, null=True, blank=True)
    position = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"


class ProductReview(AbstractBaseModel):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    rating = models.IntegerField(default=0)
    comment = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Product Review"
        verbose_name_plural = "Product Reviews"


class ProductTag(AbstractBaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="tags")
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Product Tag"
        verbose_name_plural = "Product Tags"


class ProductCollection(AbstractBaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    products = models.ManyToManyField(Product, related_name="collections")

    class Meta:
        verbose_name = "Product Collection"
        verbose_name_plural = "Product Collections"
