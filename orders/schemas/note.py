from datetime import datetime
from ninja import Schema


class OrderNoteSchema(Schema):
    id: str
    order_id: str
    note: str
    is_customer_visible: bool = False
    created_by_id: str
    meta_data: dict = {}
    created_at: datetime
    updated_at: datetime


class OrderNoteCreateSchema(Schema):
    order_id: str
    note: str
    is_customer_visible: bool = False
    meta_data: dict = {}
