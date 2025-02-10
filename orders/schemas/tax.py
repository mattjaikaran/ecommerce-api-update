from datetime import datetime
from decimal import Decimal
from typing import Optional
from ninja import Schema
from pydantic import Field


class TaxSchema(Schema):
    id: str
    order_id: str
    tax_type: str
    name: str
    rate: Decimal = Field(ge=0, le=1)
    amount: Decimal = Field(ge=0)
    jurisdiction: Optional[str] = None
    meta_data: dict = {}
    date_created: datetime
    date_updated: datetime


class TaxCreateSchema(Schema):
    tax_rate: float
    tax_amount: float
    order_id: int
    created_at: datetime
    updated_at: datetime
