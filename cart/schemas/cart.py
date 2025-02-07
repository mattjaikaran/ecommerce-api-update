from typing import List
from ninja import Schema
from datetime import datetime
from products.schemas import ProductSchema
from core.schemas import UserSchema


class CartItemSchema(Schema):
    id: int
    product: ProductSchema
    quantity: int
    price: float
    total_price: float
    created_at: datetime
    updated_at: datetime


class CartSchema(Schema):
    id: int
    user: UserSchema
    items: List[CartItemSchema]
    total_price: float
    created_at: datetime
    updated_at: datetime
