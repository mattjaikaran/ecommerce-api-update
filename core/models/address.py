"""Address model definition."""

from django.db import models

from .abstract_base import AbstractBaseModel
from .user import User


class Address(AbstractBaseModel):
    """Model for storing user addresses (billing/shipping)."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    is_default = models.BooleanField(default=False)
    is_billing = models.BooleanField(default=False)
    is_shipping = models.BooleanField(default=False)
    is_shipping_default = models.BooleanField(default=False)
    is_billing_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.address_line_1}"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Address"
        verbose_name_plural = "Addresses"
        indexes = [
            # Core lookup indexes
            models.Index(fields=["user"]),
            models.Index(fields=["is_default"]),
            models.Index(fields=["is_billing"]),
            models.Index(fields=["is_shipping"]),
            models.Index(fields=["is_billing_default"]),
            models.Index(fields=["is_shipping_default"]),
            models.Index(fields=["city"]),
            models.Index(fields=["state"]),
            models.Index(fields=["country"]),
            # Compound indexes for common queries
            models.Index(fields=["user", "is_billing"]),
            models.Index(fields=["user", "is_shipping"]),
            models.Index(fields=["user", "is_default"]),
            models.Index(fields=["country", "state"]),
        ]
