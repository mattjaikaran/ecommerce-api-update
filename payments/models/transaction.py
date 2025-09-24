"""Transaction model definition."""

from django.db import models

from core.models import AbstractBaseModel
from orders.models import Order

from .payment_method import PaymentMethod


class Transaction(AbstractBaseModel):
    """Model for storing payment transaction information."""

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=255)
    notes = models.TextField(blank=True)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=255)
    transaction_type = models.CharField(max_length=255)
    transaction_status = models.CharField(max_length=255)
    transaction_response = models.JSONField(default=dict)
    transaction_date = models.DateTimeField(auto_now_add=True)
    transaction_currency = models.CharField(max_length=255)
    transaction_amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_fee = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_tax = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_total = models.DecimalField(max_digits=10, decimal_places=2)
    # Future fields for refund tracking
    # transaction_refunded = models.DecimalField(max_digits=10, decimal_places=2)
    # transaction_refunded_date = models.DateTimeField(blank=True, null=True)
    # transaction_refunded_amount = models.DecimalField(max_digits=10, decimal_places=2)
    # transaction_refunded_currency = models.CharField(max_length=255)
    # transaction_refunded_fee = models.DecimalField(max_digits=10, decimal_places=2)
    # transaction_refunded_tax = models.DecimalField(max_digits=10, decimal_places=2)
    # transaction_refunded_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.order.id} - {self.amount}"

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
        indexes = [
            models.Index(fields=["order"]),
            models.Index(fields=["transaction_id"]),
            models.Index(fields=["transaction_status"]),
            models.Index(fields=["transaction_date"]),
            models.Index(fields=["payment_method"]),
            models.Index(fields=["amount"]),
        ]
