from datetime import datetime
from decimal import Decimal
from uuid import UUID

from ninja import Schema
from pydantic import Field, validator


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
    values: list[ProductOptionValueSchema]
    created_at: datetime
    updated_at: datetime


class ProductOptionCreateSchema(Schema):
    name: str
    position: int = 0
    values: list[ProductOptionValueSchema]


class ProductOptionUpdateSchema(Schema):
    name: str | None = None
    position: int | None = None
    values: list[ProductOptionValueSchema] | None = None


class ProductVariantOptionSchema(Schema):
    id: UUID
    option_id: UUID
    value_id: UUID
    created_at: datetime
    updated_at: datetime


class ProductImageSchema(Schema):
    id: UUID
    product_id: UUID
    variant_id: UUID | None = None
    image: str
    alt_text: str | None = None
    position: int = 0
    created_at: datetime
    updated_at: datetime


class ProductVariantSchema(Schema):
    id: UUID
    product_id: UUID
    name: str
    sku: str
    barcode: str | None = None
    price: Decimal = Field(ge=0)
    compare_at_price: Decimal | None = None
    cost_price: Decimal | None = None
    inventory_quantity: int = 0
    low_stock_threshold: int = 10
    weight: Decimal | None = None
    length: Decimal | None = None
    width: Decimal | None = None
    height: Decimal | None = None
    position: int = 0
    is_active: bool = True
    meta_data: dict = {}
    options: list[ProductVariantOptionSchema]
    images: list[ProductImageSchema]
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
    barcode: str | None = None
    price: Decimal = Field(ge=0)
    compare_at_price: Decimal | None = None
    cost_price: Decimal | None = None
    inventory_quantity: int = 0
    low_stock_threshold: int = 10
    weight: Decimal | None = None
    length: Decimal | None = None
    width: Decimal | None = None
    height: Decimal | None = None


class ProductVariantUpdateSchema(Schema):
    name: str | None = None
    sku: str | None = None
    barcode: str | None = None
    price: Decimal | None = None
    compare_at_price: Decimal | None = None
    cost_price: Decimal | None = None
    inventory_quantity: int | None = None
    low_stock_threshold: int | None = None
    weight: Decimal | None = None
    length: Decimal | None = None
    width: Decimal | None = None
    height: Decimal | None = None
