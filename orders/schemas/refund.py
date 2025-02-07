from ninja import Schema
from core.schemas import OrderSchema
from datetime import datetime


class RefundSchema(Schema):
    id: int
    order: OrderSchema
    amount: float
    status: str
    created_at: datetime
    updated_at: datetime


class RefundCreateSchema(Schema):
    order_id: int
    amount: float
    status: str
    created_at: datetime
    updated_at: datetime
