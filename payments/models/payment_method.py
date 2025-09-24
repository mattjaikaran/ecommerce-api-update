"""Payment method model definition."""

from django.db import models

from core.models import AbstractBaseModel


class PaymentMethod(AbstractBaseModel):
    """Model for storing payment method configurations."""

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    credentials = models.JSONField(default=dict)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Payment Method"
        verbose_name_plural = "Payment Methods"
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["is_active"]),
        ]
