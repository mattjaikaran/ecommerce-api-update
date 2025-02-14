from datetime import datetime
from decimal import Decimal
from typing import Optional
from ninja import Schema
from pydantic import Field
from uuid import UUID


class RefundSchema(Schema):
    id: UUID
    order_id: UUID
    transaction_id: Optional[str] = None
    amount: Decimal = Field(ge=0)
    status: str
    reason: str
    notes: Optional[str] = None
    refund_transaction_id: UUID
    gateway_response: Optional[dict] = None
    meta_data: dict = {}
    created_at: datetime
    updated_at: datetime


class RefundCreateSchema(Schema):
    order_id: UUID
    transaction_id: Optional[str] = None
    amount: Decimal = Field(ge=0)
    reason: str
    notes: Optional[str] = None
    meta_data: dict = {}


class RefundUpdateSchema(Schema):
    status: Optional[str] = None
    notes: Optional[str] = None
    meta_data: Optional[dict] = None
