from datetime import datetime
from uuid import UUID

from ninja import Schema

from core.schemas import UserSchema


class OrderHistorySchema(Schema):
    id: UUID
    order_id: UUID
    status: str
    old_status: str | None = None
    notes: str | None = None
    created_by: UserSchema
    meta_data: dict = {}
    created_at: datetime
    updated_at: datetime
