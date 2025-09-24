from datetime import datetime
from decimal import Decimal
from uuid import UUID

from ninja import Schema
from pydantic import Field


class RefundSchema(Schema):
    id: UUID
    order_id: UUID
    transaction_id: str | None = None
    amount: Decimal = Field(ge=0)
    status: str
    reason: str
    notes: str | None = None
    refund_transaction_id: UUID
    gateway_response: dict | None = None
    meta_data: dict = {}
    created_at: datetime
    updated_at: datetime


class RefundCreateSchema(Schema):
    order_id: UUID
    transaction_id: str | None = None
    amount: Decimal = Field(ge=0)
    reason: str
    notes: str | None = None
    meta_data: dict = {}


class RefundUpdateSchema(Schema):
    status: str | None = None
    notes: str | None = None
    meta_data: dict | None = None
