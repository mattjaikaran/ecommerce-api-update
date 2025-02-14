from datetime import datetime
from typing import Optional
from ninja import Schema
from core.schemas import UserSchema
from uuid import UUID


class OrderHistorySchema(Schema):
    id: UUID
    order_id: UUID
    status: str
    old_status: Optional[str] = None
    notes: Optional[str] = None
    created_by: UserSchema
    meta_data: dict = {}
    created_at: datetime
    updated_at: datetime
