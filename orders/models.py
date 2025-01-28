from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid
from core.models import AbstractBaseModel
from django.contrib.auth import get_user_model
from core.models import Address, Customer, CustomerGroup
from products.models import ProductVariant

User = get_user_model()


class OrderStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    PENDING = "pending", "Pending"
    PAID = "paid", "Paid"
    PROCESSING = "processing", "Processing"
    SHIPPED = "shipped", "Shipped"
    PARTIALLY_SHIPPED = "partially_shipped", "Partially Shipped"
    DELIVERED = "delivered", "Delivered"
    COMPLETED = "completed", "Completed"
    CANCELLED = "cancelled", "Cancelled"
    REFUNDED = "refunded", "Refunded"
    PARTIALLY_REFUNDED = "partially_refunded", "Partially Refunded"
    FAILED = "failed", "Failed"
    EXPIRED = "expired", "Expired"


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


class PaymentMethod(models.TextChoices):
    CREDIT_CARD = "credit_card", "Credit Card"
    DEBIT_CARD = "debit_card", "Debit Card"
    PAYPAL = "paypal", "PayPal"
    STRIPE = "stripe", "Stripe"
    BANK_TRANSFER = "bank_transfer", "Bank Transfer"
    CASH_ON_DELIVERY = "cash_on_delivery", "Cash on Delivery"
    CRYPTO = "crypto", "Cryptocurrency"


class ShippingMethod(models.TextChoices):
    STANDARD = "standard", "Standard Shipping"
    EXPRESS = "express", "Express Shipping"
    OVERNIGHT = "overnight", "Overnight Shipping"
    FREE = "free", "Free Shipping"
    PICKUP = "pickup", "Local Pickup"
    DIGITAL = "digital", "Digital Delivery"


class Order(AbstractBaseModel):
    """
    Model representing an order.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_number = models.CharField(max_length=32, unique=True)
    customer = models.ForeignKey(
        Customer, on_delete=models.PROTECT, related_name="orders"
    )
    customer_group = models.ForeignKey(
        CustomerGroup,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
    )
    status = models.CharField(
        max_length=50, choices=OrderStatus.choices, default=OrderStatus.DRAFT
    )
    currency = models.CharField(max_length=3, default="USD")
    subtotal = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, validators=[MinValueValidator(0)]
    )
    shipping_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, validators=[MinValueValidator(0)]
    )
    shipping_method = models.CharField(
        max_length=50, choices=ShippingMethod.choices, default=ShippingMethod.STANDARD
    )
    shipping_tax_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, validators=[MinValueValidator(0)]
    )
    discount_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, validators=[MinValueValidator(0)]
    )
    tax_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, validators=[MinValueValidator(0)]
    )
    total = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, validators=[MinValueValidator(0)]
    )
    payment_status = models.CharField(
        max_length=50, choices=PaymentStatus.choices, default=PaymentStatus.PENDING
    )
    payment_method = models.CharField(
        max_length=50, choices=PaymentMethod.choices, default=PaymentMethod.CREDIT_CARD
    )
    payment_gateway = models.CharField(max_length=50, blank=True, null=True)
    payment_gateway_id = models.CharField(max_length=255, blank=True, null=True)
    payment_gateway_response = models.JSONField(blank=True, null=True)
    billing_address = models.ForeignKey(
        Address, on_delete=models.PROTECT, related_name="billing_orders"
    )
    shipping_address = models.ForeignKey(
        Address, on_delete=models.PROTECT, related_name="shipping_orders"
    )
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True, null=True)
    customer_note = models.TextField(blank=True, null=True)
    staff_notes = models.TextField(blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    meta_data = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"Order {self.order_number}"

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ["-date_created"]
        indexes = [
            models.Index(fields=["order_number"]),
            models.Index(fields=["status"]),
            models.Index(fields=["payment_status"]),
            models.Index(fields=["date_created"]),
        ]


class OrderLineItem(AbstractBaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product_variant = models.ForeignKey(
        ProductVariant, on_delete=models.PROTECT, related_name="order_items"
    )
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    subtotal = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    discount_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, validators=[MinValueValidator(0)]
    )
    tax_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, validators=[MinValueValidator(0)]
    )
    total = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    tax_rate = models.DecimalField(
        max_digits=6,
        decimal_places=4,
        default=0.00,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
    )
    weight = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, validators=[MinValueValidator(0)]
    )
    meta_data = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"Order {self.order.order_number} - {self.product_variant.name}"

    class Meta:
        verbose_name = "Order Line Item"
        verbose_name_plural = "Order Line Items"
        ordering = ["id"]
        indexes = [
            models.Index(fields=["order", "product_variant"]),
        ]


class FulfillmentStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    PROCESSING = "processing", "Processing"
    SHIPPED = "shipped", "Shipped"
    DELIVERED = "delivered", "Delivered"
    COMPLETED = "completed", "Completed"
    CANCELLED = "cancelled", "Cancelled"
    FAILED = "failed", "Failed"


class FulfillmentOrder(AbstractBaseModel):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="fulfillments"
    )
    status = models.CharField(
        max_length=50,
        choices=FulfillmentStatus.choices,
        default=FulfillmentStatus.PENDING,
    )
    tracking_number = models.CharField(max_length=255, blank=True, null=True)
    tracking_url = models.URLField(blank=True, null=True)
    shipping_carrier = models.CharField(max_length=100, blank=True, null=True)
    shipping_method = models.CharField(
        max_length=50, choices=ShippingMethod.choices, default=ShippingMethod.STANDARD
    )
    shipping_label_url = models.URLField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    meta_data = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"Fulfillment {self.id} for Order {self.order.order_number}"

    class Meta:
        verbose_name = "Fulfillment Order"
        verbose_name_plural = "Fulfillment Orders"
        ordering = ["-date_created"]
        indexes = [
            models.Index(fields=["order", "status"]),
            models.Index(fields=["tracking_number"]),
        ]


class FulfillmentLineItem(AbstractBaseModel):
    fulfillment = models.ForeignKey(
        FulfillmentOrder, on_delete=models.CASCADE, related_name="items"
    )
    order_item = models.ForeignKey(
        OrderLineItem, on_delete=models.CASCADE, related_name="fulfillment_items"
    )
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    meta_data = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"Fulfillment Item {self.id} for Order {self.fulfillment.order.order_number}"

    class Meta:
        verbose_name = "Fulfillment Line Item"
        verbose_name_plural = "Fulfillment Line Items"
        ordering = ["id"]
        indexes = [
            models.Index(fields=["fulfillment", "order_item"]),
        ]


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
        ordering = ["-date_created"]
        indexes = [
            models.Index(fields=["order", "status"]),
            models.Index(fields=["transaction_id"]),
        ]


class RefundStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    PROCESSING = "processing", "Processing"
    COMPLETED = "completed", "Completed"
    FAILED = "failed", "Failed"
    CANCELLED = "cancelled", "Cancelled"


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
        return f"Refund {self.id} for Order {self.order.order_number}"

    class Meta:
        verbose_name = "Refund"
        verbose_name_plural = "Refunds"
        ordering = ["-date_created"]
        indexes = [
            models.Index(fields=["order", "status"]),
            models.Index(fields=["refund_transaction_id"]),
        ]


class TaxType(models.TextChoices):
    SALES = "sales", "Sales Tax"
    VAT = "vat", "Value Added Tax"
    GST = "gst", "Goods and Services Tax"
    HST = "hst", "Harmonized Sales Tax"
    PST = "pst", "Provincial Sales Tax"
    CUSTOM = "custom", "Custom Tax"


class Tax(AbstractBaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="taxes")
    tax_type = models.CharField(
        max_length=50, choices=TaxType.choices, default=TaxType.SALES
    )
    name = models.CharField(max_length=100)
    rate = models.DecimalField(
        max_digits=6,
        decimal_places=4,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
    )
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    jurisdiction = models.CharField(max_length=100, blank=True, null=True)
    meta_data = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"{self.name} for Order {self.order.order_number}"

    class Meta:
        verbose_name = "Tax"
        verbose_name_plural = "Taxes"
        ordering = ["id"]
        indexes = [
            models.Index(fields=["order", "tax_type"]),
        ]


class OrderNote(AbstractBaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="notes")
    note = models.TextField()
    is_customer_visible = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="order_notes"
    )
    meta_data = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"Note {self.id} for Order {self.order.order_number}"

    class Meta:
        verbose_name = "Order Note"
        verbose_name_plural = "Order Notes"
        ordering = ["-date_created"]
        indexes = [
            models.Index(fields=["order", "is_customer_visible"]),
        ]


class OrderHistory(AbstractBaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="history")
    status = models.CharField(max_length=50, choices=OrderStatus.choices)
    old_status = models.CharField(
        max_length=50, choices=OrderStatus.choices, null=True, blank=True
    )
    notes = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="order_status_changes"
    )
    meta_data = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"History {self.id} for Order {self.order.order_number}"

    class Meta:
        verbose_name = "Order History"
        verbose_name_plural = "Order Histories"
        ordering = ["-date_created"]
        indexes = [
            models.Index(fields=["order", "status"]),
        ]


class OrderDiscount(AbstractBaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Order Discount {self.id}"

    class Meta:
        verbose_name = "Order Discount"
        verbose_name_plural = "Order Discounts"


class OrderPayment(AbstractBaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Order Payment {self.id}"

    class Meta:
        verbose_name = "Order Payment"
        verbose_name_plural = "Order Payments"


class OrderFulfillment(AbstractBaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    fulfillment_order = models.ForeignKey(FulfillmentOrder, on_delete=models.CASCADE)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Order Fulfillment {self.id}"

    class Meta:
        verbose_name = "Order Fulfillment"
        verbose_name_plural = "Order Fulfillments"


class OrderTax(AbstractBaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    tax = models.ForeignKey(Tax, on_delete=models.CASCADE)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Order Tax {self.id}"

    class Meta:
        verbose_name = "Order Tax"
        verbose_name_plural = "Order Taxes"


class OrderFulfillmentItem(AbstractBaseModel):
    fulfillment_order = models.ForeignKey(FulfillmentOrder, on_delete=models.CASCADE)
    order_line_item = models.ForeignKey(OrderLineItem, on_delete=models.CASCADE)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Order Fulfillment Item {self.id}"

    class Meta:
        verbose_name = "Order Fulfillment Item"
        verbose_name_plural = "Order Fulfillment Items"


class OrderFulfillmentTracking(AbstractBaseModel):
    fulfillment_order = models.ForeignKey(FulfillmentOrder, on_delete=models.CASCADE)
    tracking_number = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Order Fulfillment Tracking {self.id}"

    class Meta:
        verbose_name = "Order Fulfillment Tracking"
        verbose_name_plural = "Order Fulfillment Trackings"


class OrderFulfillmentTrackingUrl(AbstractBaseModel):
    fulfillment_tracking = models.ForeignKey(
        OrderFulfillmentTracking, on_delete=models.CASCADE
    )
    url = models.URLField()
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Order Fulfillment Tracking URL {self.id}"

    class Meta:
        verbose_name = "Order Fulfillment Tracking URL"
        verbose_name_plural = "Order Fulfillment Tracking URLs"
