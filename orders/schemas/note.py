from datetime import datetime
from ninja import Schema


class OrderNoteSchema(Schema):
    id: str
    order_id: str
    note: str
    is_customer_visible: bool = False
    created_by_id: str
    meta_data: dict = {}
    date_created: datetime
    date_updated: datetime


class OrderNoteCreateSchema(Schema):
    order_id: str
    note: str
    is_customer_visible: bool = False
    meta_data: dict = {}
