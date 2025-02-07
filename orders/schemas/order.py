from ninja import Schema
from datetime import datetime
from core.schemas import UserSchema


class OrderSchema(Schema):
    id: int
    user: UserSchema
    order_date: datetime
    total_amount: float
    status: str
    created_at: datetime
    updated_at: datetime


class OrderCreateSchema(Schema):
    user_id: int
    total_amount: float
    status: str
    created_at: datetime
    updated_at: datetime


class OrderUpdateSchema(Schema):
    user_id: int
    total_amount: float
    status: str
    created_at: datetime
    updated_at: datetime
