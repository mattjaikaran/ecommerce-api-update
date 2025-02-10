from typing import Optional
from uuid import UUID
from datetime import datetime
from decimal import Decimal
from ninja import Schema


class InventoryHistorySchema(Schema):
    id: UUID
    product_id: UUID
    variant_id: Optional[UUID]
    action: str
    quantity: int
    previous_quantity: int
    new_quantity: int
    reference: Optional[str]
    notes: Optional[str]
    date_created: datetime
    date_modified: datetime


class InventoryAdjustmentSchema(Schema):
    variant_id: Optional[UUID]
    quantity: Optional[int]
    new_quantity: Optional[int]
    reference: Optional[str]
    notes: Optional[str]


class InventoryAdjustmentResponseSchema(Schema):
    success: bool
    message: str
    history: InventoryHistorySchema


class LowStockAlertSchema(Schema):
    product_id: UUID
    variant_id: Optional[UUID]
    current_quantity: int
    threshold: int
    last_restock_date: Optional[datetime]
    average_daily_sales: Optional[Decimal]
    suggested_reorder_quantity: Optional[int]


class InventorySnapshotSchema(Schema):
    product_id: UUID
    variant_id: Optional[UUID]
    quantity: int
    reserved_quantity: int
    available_quantity: int
    pending_restocks: int
    pending_orders: int
    snapshot_date: datetime
