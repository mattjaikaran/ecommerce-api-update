from datetime import datetime
from decimal import Decimal
from uuid import UUID

from ninja import Schema
from pydantic import Field


class TaxSchema(Schema):
    id: UUID
    order_id: UUID
    tax_type: str
    name: str
    rate: Decimal = Field(ge=0, le=1)
    amount: Decimal = Field(ge=0)
    jurisdiction: str | None = None
    meta_data: dict = {}
    created_at: datetime
    updated_at: datetime


class TaxCreateSchema(Schema):
    order_id: UUID
    tax_type: str
    name: str
    rate: Decimal = Field(ge=0, le=1)
    amount: Decimal = Field(ge=0)
    jurisdiction: str | None = None
    meta_data: dict = {}
