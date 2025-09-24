"""Payment-related choices and enums."""

from django.db import models


class PaymentStatus(models.TextChoices):
    """Payment status choices."""

    PENDING = "pending", "Pending"
    AUTHORIZED = "authorized", "Authorized"
    PAID = "paid", "Paid"
    PARTIALLY_PAID = "partially_paid", "Partially Paid"
    REFUNDED = "refunded", "Refunded"
    PARTIALLY_REFUNDED = "partially_refunded", "Partially Refunded"
    FAILED = "failed", "Failed"
    EXPIRED = "expired", "Expired"
    CANCELLED = "cancelled", "Cancelled"


class PaymentGateway(models.TextChoices):
    """Payment gateway choices."""

    STRIPE = "stripe", "Stripe"
    BRAVE_PAY = "brave_pay", "Brave Pay"
    PAYPAL = "paypal", "PayPal"
    CREDIT_CARD = "credit_card", "Credit Card"
    DEBIT_CARD = "debit_card", "Debit Card"
