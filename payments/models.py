from django.db import models

from core.models import AbstractBaseModel
from orders.models import Order

### Payments
# - [ ] PaymentMethod Model
#     - Payment gateway info
#     - Credentials
# - [ ] Transaction Model
#     - Payment processing
#     - Status tracking
# - [ ] Refund Model
#     - Refund processing
#     - Status tracking


class PaymentStatus(models.TextChoices):
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
    STRIPE = "stripe", "Stripe"
    BRAVE_PAY = "brave_pay", "Brave Pay"
    PAYPAL = "paypal", "PayPal"
    CREDIT_CARD = "credit_card", "Credit Card"
    DEBIT_CARD = "debit_card", "Debit Card"


class PaymentMethod(AbstractBaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    credentials = models.JSONField(default=dict)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Payment Method"
        verbose_name_plural = "Payment Methods"


class Transaction(AbstractBaseModel):
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


class Refund(AbstractBaseModel):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=255)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.transaction.id} - {self.amount}"

    class Meta:
        verbose_name = "Refund"
        verbose_name_plural = "Refunds"
