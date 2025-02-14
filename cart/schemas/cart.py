from typing import List, Optional
from ninja import Schema
from datetime import datetime
from uuid import UUID
from products.schemas import ProductVariantSchema
from core.schemas import UserSchema, CustomerSchema


class CartItemSchema(Schema):
    id: Optional[UUID] = None
    cart: Optional[UUID] = None
    product_variant: Optional[ProductVariantSchema] = None
    quantity: int = 1
    price: float = 0.0
    total_price: float = 0.0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: Optional[UserSchema] = None
    updated_by: Optional[UserSchema] = None
    is_active: bool = True
    is_deleted: bool = False
    deleted_at: Optional[datetime] = None
    deleted_by: Optional[UserSchema] = None


class CartSchema(Schema):
    id: Optional[UUID] = None
    customer: Optional[CustomerSchema] = None
    items: List[CartItemSchema] = []
    session_key: Optional[str] = None
    expires_at: Optional[datetime] = None
    subtotal: float = 0.0
    total_price: float = 0.0
    total_quantity: int = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: Optional[UserSchema] = None
    updated_by: Optional[UserSchema] = None
    is_active: bool = True
    is_deleted: bool = False
    deleted_at: Optional[datetime] = None
    deleted_by: Optional[UserSchema] = None
