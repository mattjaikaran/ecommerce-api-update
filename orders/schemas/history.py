from datetime import datetime
from typing import Optional
from ninja import Schema


class OrderHistorySchema(Schema):
    id: str
    order_id: str
    status: str
    old_status: Optional[str] = None
    notes: Optional[str] = None
    created_by_id: str
    meta_data: dict = {}
    created_at: datetime
    updated_at: datetime
