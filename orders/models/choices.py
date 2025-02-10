from django.db import models


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


class FulfillmentStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    PROCESSING = "processing", "Processing"
    SHIPPED = "shipped", "Shipped"
    DELIVERED = "delivered", "Delivered"
    COMPLETED = "completed", "Completed"
    CANCELLED = "cancelled", "Cancelled"
    FAILED = "failed", "Failed"


class RefundStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    PROCESSING = "processing", "Processing"
    COMPLETED = "completed", "Completed"
    FAILED = "failed", "Failed"
    CANCELLED = "cancelled", "Cancelled"


class TaxType(models.TextChoices):
    SALES = "sales", "Sales Tax"
    VAT = "vat", "Value Added Tax"
    GST = "gst", "Goods and Services Tax"
    HST = "hst", "Harmonized Sales Tax"
    PST = "pst", "Provincial Sales Tax"
    CUSTOM = "custom", "Custom Tax"
