from datetime import datetime
from uuid import UUID

from ninja import Schema


class OrderNoteSchema(Schema):
    id: UUID
    order_id: UUID
    note: str
    is_customer_note: bool = False
    is_staff_note: bool = False
    created_at: datetime
    updated_at: datetime


class OrderNoteCreateSchema(Schema):
    order_id: UUID
    note: str
    is_customer_note: bool = False
    is_staff_note: bool = False
    meta_data: dict = {}
