from datetime import datetime
from decimal import Decimal
from typing import Optional
from ninja import Schema
from pydantic import Field


class RefundSchema(Schema):
    id: str
    order_id: str
    transaction_id: Optional[str] = None
    amount: Decimal = Field(ge=0)
    status: str
    reason: str
    notes: Optional[str] = None
    refund_transaction_id: str
    gateway_response: Optional[dict] = None
    meta_data: dict = {}
    date_created: datetime
    date_updated: datetime


class RefundCreateSchema(Schema):
    order_id: str
    transaction_id: Optional[str] = None
    amount: Decimal = Field(ge=0)
    reason: str
    notes: Optional[str] = None
    meta_data: dict = {}


class RefundUpdateSchema(Schema):
    status: Optional[str] = None
    notes: Optional[str] = None
    meta_data: Optional[dict] = None
