from datetime import datetime
from .order import OrderSchema
from ninja import Schema


class OrderHistorySchema(Schema):
    id: int
    order: OrderSchema
    status: str
    created_at: datetime
    updated_at: datetime


class OrderHistoryCreateSchema(Schema):
    order_id: int
    status: str
    created_at: datetime
    updated_at: datetime
