from ninja import Schema
from datetime import datetime
from typing import Optional, List
from pydantic import Field, validator
from decimal import Decimal


class ProductOptionValueSchema(Schema):
    id: str
    name: str
    position: int = 0
    created_at: datetime
    updated_at: datetime


class ProductOptionSchema(Schema):
    id: str
    name: str
    position: int = 0
    values: List[ProductOptionValueSchema]
    created_at: datetime
    updated_at: datetime


class ProductVariantOptionSchema(Schema):
    id: str
    option_id: str
    value_id: str
    created_at: datetime
    updated_at: datetime


class ProductImageSchema(Schema):
    id: str
    product_id: str
    variant_id: Optional[str] = None
    image: str
    alt_text: Optional[str] = None
    position: int = 0
    created_at: datetime
    updated_at: datetime


class ProductVariantSchema(Schema):
    id: str
    product_id: str
    name: str
    sku: str
    barcode: Optional[str] = None
    price: Decimal = Field(ge=0)
    compare_at_price: Optional[Decimal] = None
    cost_price: Optional[Decimal] = None
    inventory_quantity: int = 0
    low_stock_threshold: int = 10
    weight: Optional[Decimal] = None
    length: Optional[Decimal] = None
    width: Optional[Decimal] = None
    height: Optional[Decimal] = None
    position: int = 0
    is_active: bool = True
    meta_data: dict = {}
    options: List[ProductVariantOptionSchema]
    images: List[ProductImageSchema]
    created_at: datetime
    updated_at: datetime

    @validator("compare_at_price")
    def compare_at_price_must_be_greater_than_price(cls, v, values):
        if v is not None and "price" in values and v <= values["price"]:
            raise ValueError("compare_at_price must be greater than price")
        return v
