from django.db import models
from core.models import AbstractBaseModel
from .product import Product


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
