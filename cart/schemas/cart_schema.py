from datetime import datetime
from uuid import UUID

from ninja import Schema

from core.schemas import CustomerSchema, UserSchema
from products.schemas import ProductVariantSchema


class CartItemSchema(Schema):
    id: UUID | None = None
    cart: UUID | None = None
    product_variant: ProductVariantSchema | None = None
    quantity: int = 1
    price: float = 0.0
    total_price: float = 0.0
    created_at: datetime | None = None
    updated_at: datetime | None = None
    created_by: UserSchema | None = None
    updated_by: UserSchema | None = None
    is_active: bool = True
    is_deleted: bool = False
    deleted_at: datetime | None = None
    deleted_by: UserSchema | None = None


class CartSchema(Schema):
    id: UUID | None = None
    customer: CustomerSchema | None = None
    items: list[CartItemSchema] = []
    session_key: str | None = None
    expires_at: datetime | None = None
    subtotal: float = 0.0
    total_price: float = 0.0
    total_quantity: int = 0
    created_at: datetime | None = None
    updated_at: datetime | None = None
    created_by: UserSchema | None = None
    updated_by: UserSchema | None = None
    is_active: bool = True
    is_deleted: bool = False
    deleted_at: datetime | None = None
    deleted_by: UserSchema | None = None
