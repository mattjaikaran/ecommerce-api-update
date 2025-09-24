"""Global constants for the ecommerce API.

This module contains all the constants used across the application
to ensure consistency and maintainability.
"""

# API Version
API_VERSION = "v1"
API_PREFIX = f"/api/{API_VERSION}"

# Pagination
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100

# Cache Keys
CACHE_KEY_PREFIX = "ecommerce_api"
CACHE_TIMEOUT_SHORT = 300  # 5 minutes
CACHE_TIMEOUT_MEDIUM = 1800  # 30 minutes
CACHE_TIMEOUT_LONG = 3600  # 1 hour
CACHE_TIMEOUT_DAY = 86400  # 24 hours

# Redis Keys
REDIS_KEYS = {
    "user_sessions": f"{CACHE_KEY_PREFIX}:user_sessions",
    "product_cache": f"{CACHE_KEY_PREFIX}:products",
    "cart_cache": f"{CACHE_KEY_PREFIX}:carts",
    "order_cache": f"{CACHE_KEY_PREFIX}:orders",
}

# File Upload
MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".webp", ".gif"]
ALLOWED_DOCUMENT_EXTENSIONS = [".pdf", ".doc", ".docx", ".txt"]

# Email Templates
EMAIL_TEMPLATES = {
    "welcome": "emails/welcome.html",
    "order_confirmation": "emails/order_confirmation.html",
    "password_reset": "emails/password_reset.html",
    "payment_success": "emails/payment_success.html",
    "shipping_notification": "emails/shipping_notification.html",
}

# Status Choices
ORDER_STATUS_CHOICES = [
    ("pending", "Pending"),
    ("confirmed", "Confirmed"),
    ("processing", "Processing"),
    ("shipped", "Shipped"),
    ("delivered", "Delivered"),
    ("cancelled", "Cancelled"),
    ("refunded", "Refunded"),
]

PAYMENT_STATUS_CHOICES = [
    ("pending", "Pending"),
    ("authorized", "Authorized"),
    ("captured", "Captured"),
    ("failed", "Failed"),
    ("cancelled", "Cancelled"),
    ("refunded", "Refunded"),
]

FULFILLMENT_STATUS_CHOICES = [
    ("pending", "Pending"),
    ("processing", "Processing"),
    ("shipped", "Shipped"),
    ("delivered", "Delivered"),
    ("returned", "Returned"),
]

# Currency
DEFAULT_CURRENCY = "USD"
SUPPORTED_CURRENCIES = ["USD", "EUR", "GBP", "CAD", "AUD"]

# Tax
DEFAULT_TAX_RATE = 0.08  # 8%
TAX_EXEMPT_STATES = ["OR", "MT", "NH", "DE"]

# Shipping
FREE_SHIPPING_THRESHOLD = 50.00
DEFAULT_SHIPPING_COST = 9.99
EXPRESS_SHIPPING_COST = 19.99

# Product
PRODUCT_SLUG_MAX_LENGTH = 255
PRODUCT_NAME_MAX_LENGTH = 255
PRODUCT_DESCRIPTION_MAX_LENGTH = 2000

# Inventory
LOW_STOCK_THRESHOLD = 10
OUT_OF_STOCK_THRESHOLD = 0

# User
USERNAME_MAX_LENGTH = 150
PHONE_NUMBER_MAX_LENGTH = 20

# Security
SESSION_TIMEOUT = 1800  # 30 minutes
MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_DURATION = 900  # 15 minutes

# Error Messages
ERROR_MESSAGES = {
    "invalid_credentials": "Invalid email or password.",
    "account_locked": "Account temporarily locked due to too many failed login attempts.",
    "insufficient_stock": "Insufficient stock for this product.",
    "invalid_coupon": "Invalid or expired coupon code.",
    "payment_failed": "Payment processing failed. Please try again.",
    "shipping_unavailable": "Shipping is not available to this address.",
}

# Success Messages
SUCCESS_MESSAGES = {
    "account_created": "Account created successfully.",
    "password_updated": "Password updated successfully.",
    "order_placed": "Order placed successfully.",
    "payment_processed": "Payment processed successfully.",
    "profile_updated": "Profile updated successfully.",
}

# External Services
STRIPE_WEBHOOK_TOLERANCE = 300  # 5 minutes
SENDGRID_TIMEOUT = 30  # seconds
AWS_S3_TIMEOUT = 60  # seconds

# Logging
LOG_LEVELS = {
    "DEBUG": 10,
    "INFO": 20,
    "WARNING": 30,
    "ERROR": 40,
    "CRITICAL": 50,
}

# Health Check
HEALTH_CHECK_SERVICES = [
    "database",
    "redis",
    "s3",
    "stripe",
]

# Rate Limiting
RATE_LIMIT_PER_MINUTE = 60
RATE_LIMIT_PER_HOUR = 1000
RATE_LIMIT_PER_DAY = 10000

# Search
SEARCH_RESULTS_PER_PAGE = 20
MAX_SEARCH_RESULTS = 1000
SEARCH_TIMEOUT = 5  # seconds
