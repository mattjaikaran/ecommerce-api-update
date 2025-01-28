from django.db import models
import uuid
from core.models import AbstractBaseModel
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


class ProductStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    ACTIVE = "active", "Active"
    ARCHIVED = "archived", "Archived"


class ProductType(models.TextChoices):
    PHYSICAL = "physical", "Physical"
    DIGITAL = "digital", "Digital"
    SERVICE = "service", "Service"


class TaxClass(models.TextChoices):
    STANDARD = "standard", "Standard"
    REDUCED = "reduced", "Reduced"
    ZERO = "zero", "Zero"


class ShippingClass(models.TextChoices):
    STANDARD = "standard", "Standard"
    EXPRESS = "express", "Express"
    FREE = "free", "Free"


class ProductCategory(AbstractBaseModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, related_name="children", null=True, blank=True
    )
    image = models.ImageField(upload_to="categories/", null=True, blank=True)
    seo_title = models.CharField(max_length=255, null=True, blank=True)
    seo_description = models.TextField(null=True, blank=True)
    seo_keywords = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    position = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Product Category"
        verbose_name_plural = "Product Categories"
        ordering = ["position", "name"]


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
        ordering = ["-date_created"]


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


class ProductReview(AbstractBaseModel):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    title = models.CharField(max_length=255)
    comment = models.TextField()
    is_verified = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Product Review"
        verbose_name_plural = "Product Reviews"
        ordering = ["-date_created"]
        unique_together = ["product", "user"]


class ProductTag(AbstractBaseModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    products = models.ManyToManyField(Product, related_name="tags")

    class Meta:
        verbose_name = "Product Tag"
        verbose_name_plural = "Product Tags"
        ordering = ["name"]


class ProductCollection(AbstractBaseModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="collections/", null=True, blank=True)
    products = models.ManyToManyField(Product, related_name="collections")
    is_active = models.BooleanField(default=True)
    position = models.IntegerField(default=0)
    seo_title = models.CharField(max_length=255, null=True, blank=True)
    seo_description = models.TextField(null=True, blank=True)
    seo_keywords = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Product Collection"
        verbose_name_plural = "Product Collections"
        ordering = ["position", "name"]
