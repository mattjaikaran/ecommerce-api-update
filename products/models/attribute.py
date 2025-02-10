from django.db import models
from django.core.exceptions import ValidationError
from core.models import AbstractBaseModel
from .product import Product
from .choices import AttributeDisplayType, AttributeValidationType


class ProductAttribute(AbstractBaseModel):
    name = models.CharField(max_length=255)
    code = models.SlugField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    is_filterable = models.BooleanField(default=True)
    is_searchable = models.BooleanField(default=True)
    is_required = models.BooleanField(default=False)
    is_visible = models.BooleanField(default=True)
    is_variation = models.BooleanField(default=False)
    position = models.IntegerField(default=0)
    display_type = models.CharField(
        max_length=50,
        choices=AttributeDisplayType.choices,
        default=AttributeDisplayType.TEXT,
    )
    validation_type = models.CharField(
        max_length=50,
        choices=AttributeValidationType.choices,
        default=AttributeValidationType.NONE,
    )
    validation_regex = models.CharField(max_length=255, null=True, blank=True)
    validation_message = models.CharField(max_length=255, null=True, blank=True)
    default_value = models.CharField(max_length=255, null=True, blank=True)
    min_value = models.CharField(max_length=255, null=True, blank=True)
    max_value = models.CharField(max_length=255, null=True, blank=True)
    unit = models.CharField(max_length=50, null=True, blank=True)
    help_text = models.CharField(max_length=255, null=True, blank=True)
    icon = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Product Attribute"
        verbose_name_plural = "Product Attributes"
        ordering = ["position", "name"]

    def get_values(self):
        """Get all values for this attribute"""
        return self.values.all().order_by("position")

    def get_active_values(self):
        """Get all active values for this attribute"""
        return self.values.filter(is_active=True).order_by("position")

    def get_products(self):
        """Get all products that have this attribute"""
        return Product.objects.filter(attributes__attribute=self).distinct()

    def get_value_counts(self):
        """Get counts of how many products use each value"""
        from django.db.models import Count

        return self.values.annotate(
            product_count=Count("productattributeassignment__product", distinct=True)
        ).order_by("-product_count")

    def validate_value(self, value):
        """Validate a value against this attribute's validation rules"""
        import re
        from django.core.validators import validate_email, URLValidator

        if not value:
            if self.is_required:
                raise ValidationError("This field is required.")
            return True

        if self.validation_type == AttributeValidationType.NUMBER:
            try:
                int(value)
                if self.min_value and int(value) < int(self.min_value):
                    raise ValidationError(
                        f"Value must be greater than {self.min_value}."
                    )
                if self.max_value and int(value) > int(self.max_value):
                    raise ValidationError(f"Value must be less than {self.max_value}.")
            except ValueError:
                raise ValidationError("Value must be a number.")

        elif self.validation_type == AttributeValidationType.DECIMAL:
            try:
                float(value)
                if self.min_value and float(value) < float(self.min_value):
                    raise ValidationError(
                        f"Value must be greater than {self.min_value}."
                    )
                if self.max_value and float(value) > float(self.max_value):
                    raise ValidationError(f"Value must be less than {self.max_value}.")
            except ValueError:
                raise ValidationError("Value must be a decimal number.")

        elif self.validation_type == AttributeValidationType.EMAIL:
            validate_email(value)

        elif self.validation_type == AttributeValidationType.URL:
            URLValidator()(value)

        elif (
            self.validation_type == AttributeValidationType.REGEX
            and self.validation_regex
        ):
            if not re.match(self.validation_regex, value):
                raise ValidationError(
                    self.validation_message
                    or "Value does not match the required pattern."
                )

        return True


class ProductAttributeValue(AbstractBaseModel):
    attribute = models.ForeignKey(
        ProductAttribute, on_delete=models.CASCADE, related_name="values"
    )
    value = models.CharField(max_length=255)
    display_value = models.CharField(max_length=255, null=True, blank=True)
    position = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)
    color_code = models.CharField(max_length=50, null=True, blank=True)
    image = models.ImageField(upload_to="attributes/values/", null=True, blank=True)
    icon = models.CharField(max_length=50, null=True, blank=True)
    tooltip = models.CharField(max_length=255, null=True, blank=True)
    meta_data = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"{self.attribute.name}: {self.value}"

    class Meta:
        verbose_name = "Product Attribute Value"
        verbose_name_plural = "Product Attribute Values"
        ordering = ["position"]
        unique_together = ["attribute", "value"]

    def get_products(self):
        """Get all products that have this attribute value"""
        return Product.objects.filter(attributes__value=self).distinct()

    def get_display_value(self):
        """Get the display value, falling back to the actual value if not set"""
        return self.display_value or self.value

    def get_swatch_data(self):
        """Get swatch data based on the attribute display type"""
        if self.attribute.display_type == AttributeDisplayType.COLOR:
            return {"type": "color", "value": self.color_code}
        elif self.attribute.display_type == AttributeDisplayType.IMAGE:
            return {"type": "image", "url": self.image.url if self.image else None}
        return None

    def validate(self):
        """Validate this value against the attribute's validation rules"""
        return self.attribute.validate_value(self.value)

    def save(self, *args, **kwargs):
        # Validate the value before saving
        self.validate()

        # If this is marked as default, unmark other default values
        if self.is_default:
            type(self).objects.filter(attribute=self.attribute, is_default=True).update(
                is_default=False
            )

        # If no display value is set, use the actual value
        if not self.display_value:
            self.display_value = self.value

        super().save(*args, **kwargs)


class ProductAttributeAssignment(AbstractBaseModel):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="attributes"
    )
    attribute = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE)
    value = models.ForeignKey(ProductAttributeValue, on_delete=models.CASCADE)
    position = models.IntegerField(default=0)
    is_visible = models.BooleanField(default=True)
    is_variation = models.BooleanField(default=False)
    price_adjustment = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Price adjustment when this value is selected",
    )
    weight_adjustment = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Weight adjustment when this value is selected",
    )
    meta_data = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"{self.product.name} - {self.attribute.name}: {self.value.value}"

    class Meta:
        verbose_name = "Product Attribute Assignment"
        verbose_name_plural = "Product Attribute Assignments"
        ordering = ["position"]
        unique_together = ["product", "attribute"]

    def get_adjusted_price(self, base_price):
        """Calculate the adjusted price based on this attribute value"""
        if self.price_adjustment is None:
            return base_price
        return base_price + self.price_adjustment

    def get_adjusted_weight(self, base_weight):
        """Calculate the adjusted weight based on this attribute value"""
        if self.weight_adjustment is None or base_weight is None:
            return base_weight
        return base_weight + self.weight_adjustment

    def validate(self):
        """Validate this assignment"""
        # Validate that the value belongs to the attribute
        if self.value.attribute_id != self.attribute_id:
            raise ValidationError("Value does not belong to the specified attribute.")

        # Validate the value itself
        self.value.validate()

        return True

    def save(self, *args, **kwargs):
        # Validate before saving
        self.validate()

        # If this is a variation attribute, mark it as such
        if self.attribute.is_variation:
            self.is_variation = True

        super().save(*args, **kwargs)
