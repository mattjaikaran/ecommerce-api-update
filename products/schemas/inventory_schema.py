from datetime import datetime
from decimal import Decimal
from uuid import UUID

from ninja import Schema


class InventoryHistorySchema(Schema):
    id: UUID
    product_id: UUID
    variant_id: UUID | None
    action: str
    quantity: int
    previous_quantity: int
    new_quantity: int
    reference: str | None
    notes: str | None
    created_at: datetime
    date_modified: datetime


class InventoryAdjustmentSchema(Schema):
    variant_id: UUID | None
    quantity: int | None
    new_quantity: int | None
    reference: str | None
    notes: str | None


class InventoryAdjustmentResponseSchema(Schema):
    success: bool
    message: str
    history: InventoryHistorySchema


class LowStockAlertSchema(Schema):
    product_id: UUID
    variant_id: UUID | None
    current_quantity: int
    threshold: int
    last_restock_date: datetime | None
    average_daily_sales: Decimal | None
    suggested_reorder_quantity: int | None


class InventorySnapshotSchema(Schema):
    product_id: UUID
    variant_id: UUID | None
    quantity: int
    reserved_quantity: int
    available_quantity: int
    pending_restocks: int
    pending_orders: int
    snapshot_date: datetime
