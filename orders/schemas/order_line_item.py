from datetime import datetime
from decimal import Decimal
from ninja import Schema
from pydantic import Field
from uuid import UUID


class OrderLineItemSchema(Schema):
    id: UUID
    product_variant_id: UUID
    quantity: int = Field(ge=1)
    unit_price: Decimal = Field(ge=0)
    subtotal: Decimal = Field(ge=0)
    discount_amount: Decimal = Field(ge=0)
    tax_amount: Decimal = Field(ge=0)
    total: Decimal = Field(ge=0)
    tax_rate: Decimal = Field(ge=0, le=1)
    weight: Decimal = Field(ge=0)
    meta_data: dict = {}
    created_at: datetime
    updated_at: datetime


class OrderLineItemCreateSchema(Schema):
    product_variant_id: UUID
    quantity: int = Field(ge=1)


class OrderLineItemUpdateSchema(Schema):
    quantity: int = Field(ge=1)
