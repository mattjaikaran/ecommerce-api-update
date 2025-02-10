from ninja import Schema
from datetime import datetime
from .order import OrderSchema
from decimal import Decimal
from typing import Optional
from pydantic import Field


class PaymentSchema(Schema):
    id: int
    order: OrderSchema
    amount: float
    status: str
    created_at: datetime
    updated_at: datetime


class PaymentCreateSchema(Schema):
    amount: float
    status: str
    created_at: datetime
    updated_at: datetime


class PaymentTransactionSchema(Schema):
    id: str
    order_id: str
    transaction_id: str
    payment_method: str
    amount: Decimal = Field(ge=0)
    currency: str = "USD"
    status: str
    gateway: str
    gateway_response: Optional[dict] = None
    error_message: Optional[str] = None
    meta_data: dict = {}
    date_created: datetime
    date_updated: datetime
