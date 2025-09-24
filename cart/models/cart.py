"""Cart model definition."""

from django.db import models

from core.models import AbstractBaseModel, Customer


class Cart(AbstractBaseModel):
    """Shopping cart model for storing customer cart information."""

    session_key = models.CharField(max_length=255, null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, null=True, blank=True
    )
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_quantity = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Cart {self.id}"

    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Carts"
        indexes = [
            # Core lookup indexes
            models.Index(fields=["session_key"]),
            models.Index(fields=["customer"]),
            models.Index(fields=["is_active"]),
            models.Index(fields=["expires_at"]),
            # Date-based indexes
            models.Index(fields=["created_at"]),
            models.Index(fields=["updated_at"]),
            # Compound indexes for common queries
            models.Index(fields=["customer", "is_active"]),
            models.Index(fields=["session_key", "is_active"]),
            models.Index(fields=["expires_at", "is_active"]),
        ]
