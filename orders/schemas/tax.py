from ninja import Schema
from datetime import datetime
from .order import OrderSchema


class TaxSchema(Schema):
    id: int
    order: OrderSchema
    tax_rate: float
    tax_amount: float
    created_at: datetime
    updated_at: datetime


class TaxCreateSchema(Schema):
    tax_rate: float
    tax_amount: float
    order_id: int
    created_at: datetime
    updated_at: datetime
