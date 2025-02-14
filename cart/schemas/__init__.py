from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from ninja import Schema
from uuid import UUID
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


class CartSchema(Schema):
    id: UUID
    customer_id: Optional[UUID] = None
    session_key: Optional[str] = None
    expires_at: Optional[datetime] = None
    subtotal: Decimal = Field(ge=0)
    total_price: Decimal = Field(ge=0)
    total_quantity: int = Field(ge=0)
    is_active: bool = True
    items: List[CartItemSchema]
    created_at: datetime
    updated_at: datetime


__all__ = [
    "CartSchema",
    "CartItemSchema",
    "CartItemCreateSchema",
    "CartItemUpdateSchema",
]
