from datetime import datetime

from ninja import Schema

from .order import OrderSchema


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
