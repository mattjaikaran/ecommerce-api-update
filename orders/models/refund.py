from django.db import models
from django.core.validators import MinValueValidator
from core.models import AbstractBaseModel
from .order import Order
from .payment import PaymentTransaction
from .choices import RefundStatus


class Refund(AbstractBaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="refunds")
    transaction = models.ForeignKey(
        PaymentTransaction, on_delete=models.SET_NULL, null=True, related_name="refunds"
    )
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    status = models.CharField(
        max_length=50, choices=RefundStatus.choices, default=RefundStatus.PENDING
    )
    reason = models.TextField()
    notes = models.TextField(blank=True, null=True)
    refund_transaction_id = models.CharField(max_length=255, unique=True)
    gateway_response = models.JSONField(blank=True, null=True)
    meta_data = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return (
            f"Refund {self.refund_transaction_id} for Order {self.order.order_number}"
        )

    class Meta:
        verbose_name = "Refund"
        verbose_name_plural = "Refunds"
        ordering = ["-date_created"]
        indexes = [
            models.Index(fields=["order", "refund_transaction_id"]),
            models.Index(fields=["status"]),
            models.Index(fields=["date_created"]),
        ]
