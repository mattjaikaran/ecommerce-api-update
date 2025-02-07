from ninja import Schema
from datetime import datetime
from .order import OrderSchema


class PaymentSchema(Schema):
    id: int
    order: OrderSchema
    amount: float
    status: str
    created_at: datetime
    updated_at: datetime


class PaymentCreateSchema(Schema):
    amount: float
    status: str
    created_at: datetime
    updated_at: datetime
