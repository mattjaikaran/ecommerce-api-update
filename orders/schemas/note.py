from datetime import datetime
from ninja import Schema
from core.schemas import UserSchema


class OrderNoteSchema(Schema):
    id: str
    order_id: str
    note: str
    is_customer_visible: bool = False
    created_by: UserSchema
    meta_data: dict = {}
    created_at: datetime
    updated_at: datetime


class OrderNoteCreateSchema(Schema):
    order_id: str
    note: str
    is_customer_visible: bool = False
    meta_data: dict = {}
