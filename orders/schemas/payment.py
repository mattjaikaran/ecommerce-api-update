from ninja import Schema
from datetime import datetime
from decimal import Decimal
from uuid import UUID
from pydantic import Field


class PaymentSchema(Schema):
    id: UUID
    order_id: UUID
    amount: Decimal = Field(ge=0)
    status: str
    created_at: datetime
    updated_at: datetime


class PaymentCreateSchema(Schema):
    order_id: UUID
    amount: Decimal = Field(ge=0)
    status: str
    meta_data: dict = {}


class PaymentTransactionSchema(Schema):
    id: UUID
    order_id: UUID
    transaction_id: UUID
    amount: Decimal = Field(ge=0)
    status: str
    payment_method: str
    payment_gateway: str
    gateway_response: dict = None
    meta_data: dict = {}
    created_at: datetime
    updated_at: datetime


class PaymentTransactionCreateSchema(Schema):
    order_id: UUID
    amount: Decimal = Field(ge=0)
    payment_method: str
    payment_gateway: str
    meta_data: dict = {}
