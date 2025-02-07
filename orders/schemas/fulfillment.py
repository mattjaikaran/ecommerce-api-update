from ninja import Schema
from datetime import datetime
from .order import OrderSchema


class FulfillmentSchema(Schema):
    id: int
    order: OrderSchema
    fulfillment_date: datetime
    status: str
    created_at: datetime
    updated_at: datetime


class FulfillmentCreateSchema(Schema):
    order_id: int
    fulfillment_date: datetime
    status: str
