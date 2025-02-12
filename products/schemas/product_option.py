from ninja import Schema
from datetime import datetime
from typing import Optional, List
from pydantic import Field, validator
from decimal import Decimal
from uuid import UUID


class ProductOptionValueSchema(Schema):
    id: UUID
    name: str
    position: int = 0
    created_at: datetime
    updated_at: datetime


class ProductOptionSchema(Schema):
    id: UUID
    name: str
    position: int = 0
    values: List[ProductOptionValueSchema]
    created_at: datetime
    updated_at: datetime


class ProductOptionCreateSchema(Schema):
    name: str
    position: int = 0
    values: List[ProductOptionValueSchema]


class ProductOptionUpdateSchema(Schema):
    name: Optional[str] = None
    position: Optional[int] = None
    values: Optional[List[ProductOptionValueSchema]] = None


class ProductVariantOptionSchema(Schema):
    id: UUID
    option_id: UUID
    value_id: UUID
    created_at: datetime
    updated_at: datetime


class ProductImageSchema(Schema):
    id: UUID
    product_id: UUID
    variant_id: Optional[UUID] = None
    image: str
    alt_text: Optional[str] = None
    position: int = 0
    created_at: datetime
    updated_at: datetime


class ProductVariantSchema(Schema):
    id: UUID
    product_id: UUID
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


class ProductVariantCreateSchema(Schema):
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


class ProductVariantUpdateSchema(Schema):
    name: Optional[str] = None
    sku: Optional[str] = None
    barcode: Optional[str] = None
    price: Optional[Decimal] = None
    compare_at_price: Optional[Decimal] = None
    cost_price: Optional[Decimal] = None
    inventory_quantity: Optional[int] = None
    low_stock_threshold: Optional[int] = None
    weight: Optional[Decimal] = None
    length: Optional[Decimal] = None
    width: Optional[Decimal] = None
    height: Optional[Decimal] = None
