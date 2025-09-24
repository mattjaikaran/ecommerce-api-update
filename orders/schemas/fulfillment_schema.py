from datetime import datetime
from decimal import Decimal
from uuid import UUID

from ninja import Schema
from pydantic import Field

from orders.models import ShippingMethod


class FulfillmentLineItemSchema(Schema):
    id: UUID
    fulfillment_id: UUID
    order_item_id: UUID
    quantity: int = Field(ge=1)
    meta_data: dict = {}
    created_at: datetime
    updated_at: datetime
    date_modified: datetime | None = None


class FulfillmentOrderSchema(Schema):
    id: UUID
    order_id: UUID
    status: str
    tracking_number: str | None = None
    tracking_url: str | None = None
    shipping_label_url: str | None = None
    shipping_carrier: str | None = None
    shipping_method: str = ShippingMethod.STANDARD
    shipping_cost: Decimal = Field(ge=0, default=Decimal("0.00"))
    meta_data: dict = {}
    items: list[FulfillmentLineItemSchema]
    created_at: datetime
    updated_at: datetime
    date_modified: datetime | None = None


class FulfillmentOrderCreateSchema(Schema):
    order_id: UUID
    tracking_number: str | None = None
    tracking_url: str | None = None
    shipping_label_url: str | None = None
    shipping_carrier: str | None = None
    shipping_method: str = ShippingMethod.STANDARD
    shipping_cost: Decimal = Field(ge=0, default=Decimal("0.00"))
    meta_data: dict = {}
    items: list[dict]  # List of {order_item_id: UUID, quantity: int}


class FulfillmentLineItemCreateSchema(Schema):
    id: UUID
    order_id: UUID
    order_item_id: UUID
    quantity: int = Field(ge=1)
    meta_data: dict = {}


class FulfillmentOrderUpdateSchema(Schema):
    order_id: UUID
    status: str | None = None
    tracking_number: str | None = None
    tracking_url: str | None = None
    shipping_label_url: str | None = None
    shipping_carrier: str | None = None
    shipping_method: str | None = None
    shipping_cost: Decimal | None = None
    meta_data: dict | None = None
    items: list[dict] | None = None  # List of {order_item_id: UUID, quantity: int}


class FulfillmentSchema(Schema):
    id: UUID
    order_id: UUID
    status: str
    tracking_number: str | None = None
    tracking_url: str | None = None
    shipping_carrier: str | None = None
    shipping_method: str = ShippingMethod.STANDARD
    shipping_label_url: str | None = None
    shipping_cost: Decimal = Field(ge=0, default=Decimal("0.00"))
    notes: str | None = None
    meta_data: dict = {}
    items: list[FulfillmentLineItemSchema]
    created_at: datetime
    updated_at: datetime
    date_modified: datetime | None = None


class FulfillmentCreateSchema(Schema):
    order_id: UUID
    tracking_number: str | None = None
    tracking_url: str | None = None
    shipping_carrier: str | None = None
    shipping_method: str = ShippingMethod.STANDARD
    shipping_label_url: str | None = None
    shipping_cost: Decimal = Field(ge=0, default=Decimal("0.00"))
    notes: str | None = None
    meta_data: dict = {}
    items: list[dict]  # List of {order_item_id: UUID, quantity: int}


class FulfillmentUpdateSchema(Schema):
    status: str | None = None
    tracking_number: str | None = None
    tracking_url: str | None = None
    shipping_carrier: str | None = None
    shipping_method: str | None = None
    shipping_label_url: str | None = None
    shipping_cost: Decimal | None = None
    notes: str | None = None
    meta_data: dict | None = None
    items: list[dict] | None = None  # List of {order_item_id: UUID, quantity: int}
