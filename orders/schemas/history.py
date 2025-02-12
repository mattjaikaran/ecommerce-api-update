from datetime import datetime
from typing import Optional
from ninja import Schema
from core.schemas import UserSchema


class OrderHistorySchema(Schema):
    id: str
    order_id: str
    status: str
    old_status: Optional[str] = None
    notes: Optional[str] = None
    created_by: UserSchema
    meta_data: dict = {}
    created_at: datetime
    updated_at: datetime
