"""Refund model definition."""

from django.db import models

from core.models import AbstractBaseModel

from .transaction import Transaction


class Refund(AbstractBaseModel):
    """Model for storing payment refund information."""

    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=255)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.transaction.id} - {self.amount}"

    class Meta:
        verbose_name = "Refund"
        verbose_name_plural = "Refunds"
        indexes = [
            models.Index(fields=["transaction"]),
            models.Index(fields=["status"]),
            models.Index(fields=["amount"]),
            models.Index(fields=["created_at"]),
        ]
