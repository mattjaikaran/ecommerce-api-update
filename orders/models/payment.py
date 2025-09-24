from django.core.validators import MinValueValidator
from django.db import models

from core.models import AbstractBaseModel

from .choices import PaymentMethod, PaymentStatus
from .order import Order


class PaymentTransaction(AbstractBaseModel):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="transactions"
    )
    transaction_id = models.CharField(max_length=255, unique=True)
    payment_method = models.CharField(max_length=50, choices=PaymentMethod.choices)
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    currency = models.CharField(max_length=3, default="USD")
    status = models.CharField(
        max_length=50, choices=PaymentStatus.choices, default=PaymentStatus.PENDING
    )
    gateway = models.CharField(max_length=50)
    gateway_response = models.JSONField(blank=True, null=True)
    error_message = models.TextField(blank=True, null=True)
    meta_data = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"Payment {self.transaction_id} for Order {self.order.order_number}"

    class Meta:
        verbose_name = "Payment Transaction"
        verbose_name_plural = "Payment Transactions"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["order", "transaction_id"]),
            models.Index(fields=["status"]),
            models.Index(fields=["created_at"]),
        ]


class OrderPayment(AbstractBaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Payment for Order {self.order.order_number}"

    class Meta:
        verbose_name = "Order Payment"
        verbose_name_plural = "Order Payments"
