from ninja import Schema
from datetime import datetime
from .order import OrderSchema


class OrderNoteSchema(Schema):
    id: int
    order: OrderSchema
    note: str
    created_at: datetime
    updated_at: datetime


class OrderNoteCreateSchema(Schema):
    note: str
