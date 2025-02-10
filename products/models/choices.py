from django.db import models


class ProductStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    ACTIVE = "active", "Active"
    ARCHIVED = "archived", "Archived"


class ProductType(models.TextChoices):
    PHYSICAL = "physical", "Physical"
    DIGITAL = "digital", "Digital"
    SERVICE = "service", "Service"


class TaxClass(models.TextChoices):
    STANDARD = "standard", "Standard"
    REDUCED = "reduced", "Reduced"
    ZERO = "zero", "Zero"


class ShippingClass(models.TextChoices):
    STANDARD = "standard", "Standard"
    EXPRESS = "express", "Express"
    FREE = "free", "Free"


class InventoryAction(models.TextChoices):
    STOCK_ADD = "stock_add", "Stock Added"
    STOCK_REMOVE = "stock_remove", "Stock Removed"
    STOCK_ADJUST = "stock_adjust", "Stock Adjusted"
    ORDER_PLACED = "order_placed", "Order Placed"
    ORDER_CANCELLED = "order_cancelled", "Order Cancelled"
    RETURN = "return", "Return"


class PriceAction(models.TextChoices):
    REGULAR_PRICE = "regular_price", "Regular Price Change"
    SALE_PRICE = "sale_price", "Sale Price Change"
    COST_PRICE = "cost_price", "Cost Price Change"
    PROMOTION = "promotion", "Promotion"


class AttributeDisplayType(models.TextChoices):
    TEXT = "text", "Text"
    SELECT = "select", "Select"
    MULTISELECT = "multiselect", "Multi Select"
    RADIO = "radio", "Radio Buttons"
    CHECKBOX = "checkbox", "Checkboxes"
    COLOR = "color", "Color Swatch"
    IMAGE = "image", "Image Swatch"
    BUTTON = "button", "Button"
    RANGE = "range", "Range Slider"


class AttributeValidationType(models.TextChoices):
    NONE = "none", "None"
    NUMBER = "number", "Number"
    DECIMAL = "decimal", "Decimal"
    EMAIL = "email", "Email"
    URL = "url", "URL"
    REGEX = "regex", "Regular Expression"


class RelatedProductType(models.TextChoices):
    UPSELL = "upsell", "Upsell"
    CROSS_SELL = "cross_sell", "Cross Sell"
    ACCESSORY = "accessory", "Accessory"
    SIMILAR = "similar", "Similar"
    BUNDLE = "bundle", "Bundle"
