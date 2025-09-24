from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from ninja import Schema
from pydantic import Field


class CartItemSchema(Schema):
    id: UUID
    cart_id: UUID
    product_variant_id: UUID
    quantity: int = Field(ge=1)
    price: Decimal = Field(ge=0)
    created_at: datetime
    updated_at: datetime


class CartItemCreateSchema(Schema):
    product_variant_id: UUID
    quantity: int = Field(ge=1)


class CartItemUpdateSchema(Schema):
    quantity: int = Field(ge=1)


class CartCreateSchema(Schema):
    customer_id: UUID | None = None
    session_key: str | None = None


class CartUpdateSchema(Schema):
    customer_id: UUID | None = None
    session_key: str | None = None
    is_active: bool | None = None


class CartSchema(Schema):
    id: UUID
    customer_id: UUID | None = None
    session_key: str | None = None
    expires_at: datetime | None = None
    subtotal: Decimal = Field(ge=0)
    total_price: Decimal = Field(ge=0)
    total_quantity: int = Field(ge=0)
    is_active: bool = True
    items: list[CartItemSchema]
    created_at: datetime
    updated_at: datetime


__all__ = [
    "CartCreateSchema",
    "CartItemCreateSchema",
    "CartItemSchema",
    "CartItemUpdateSchema",
    "CartSchema",
    "CartUpdateSchema",
]
