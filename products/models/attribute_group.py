from django.db import models
from core.models import AbstractBaseModel
from .product import Product
from .attribute import ProductAttribute, ProductAttributeAssignment


class ProductAttributeGroup(AbstractBaseModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    position = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_visible = models.BooleanField(default=True)
    attributes = models.ManyToManyField(ProductAttribute, related_name="groups")
    products = models.ManyToManyField(Product, related_name="attribute_groups")
    icon = models.CharField(max_length=50, null=True, blank=True)
    display_mode = models.CharField(
        max_length=50,
        choices=[
            ("list", "List"),
            ("grid", "Grid"),
            ("dropdown", "Dropdown"),
            ("buttons", "Buttons"),
            ("swatches", "Color Swatches"),
        ],
        default="list",
    )
    is_collapsible = models.BooleanField(default=True)
    is_collapsed_by_default = models.BooleanField(default=False)
    show_product_count = models.BooleanField(default=True)
    show_search = models.BooleanField(default=False)
    min_choices = models.PositiveIntegerField(default=0)
    max_choices = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Product Attribute Group"
        verbose_name_plural = "Product Attribute Groups"
        ordering = ["position", "name"]

    def get_active_attributes(self):
        """Get all active attributes in this group"""
        return self.attributes.filter(is_active=True).order_by("position", "name")

    def get_visible_attributes(self):
        """Get all visible attributes in this group"""
        return self.attributes.filter(is_active=True, is_visible=True).order_by(
            "position", "name"
        )

    def get_filterable_attributes(self):
        """Get all filterable attributes in this group"""
        return self.attributes.filter(is_active=True, is_filterable=True).order_by(
            "position", "name"
        )

    def get_products_with_attributes(self):
        """Get all products that have attributes from this group"""
        return self.products.filter(
            attributes__attribute__in=self.attributes.all()
        ).distinct()

    def get_attribute_value_counts(self):
        """Get counts of how many products use each attribute value"""
        from django.db.models import Count

        return (
            ProductAttributeAssignment.objects.filter(
                product__in=self.products.all(), attribute__in=self.attributes.all()
            )
            .values("attribute__name", "value__value")
            .annotate(count=Count("product", distinct=True))
            .order_by("attribute__name", "-count")
        )
