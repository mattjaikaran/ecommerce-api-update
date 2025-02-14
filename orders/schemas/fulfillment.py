from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from ninja import Schema
from pydantic import Field
from uuid import UUID

from orders.models import ShippingMethod


class FulfillmentLineItemSchema(Schema):
    id: UUID
    fulfillment_id: UUID
    order_item_id: UUID
    quantity: int = Field(ge=1)
    meta_data: dict = {}
    created_at: datetime
    updated_at: datetime
    date_modified: Optional[datetime] = None


class FulfillmentOrderSchema(Schema):
    id: UUID
    order_id: UUID
    status: str
    tracking_number: Optional[str] = None
    tracking_url: Optional[str] = None
    shipping_label_url: Optional[str] = None
    shipping_carrier: Optional[str] = None
    shipping_method: str = ShippingMethod.STANDARD
    shipping_cost: Decimal = Field(ge=0, default=Decimal("0.00"))
    meta_data: dict = {}
    items: List[FulfillmentLineItemSchema]
    created_at: datetime
    updated_at: datetime
    date_modified: Optional[datetime] = None


class FulfillmentOrderCreateSchema(Schema):
    order_id: UUID
    tracking_number: Optional[str] = None
    tracking_url: Optional[str] = None
    shipping_label_url: Optional[str] = None
    shipping_carrier: Optional[str] = None
    shipping_method: str = ShippingMethod.STANDARD
    shipping_cost: Decimal = Field(ge=0, default=Decimal("0.00"))
    meta_data: dict = {}
    items: List[dict]  # List of {order_item_id: UUID, quantity: int}


class FulfillmentLineItemCreateSchema(Schema):
    id: UUID
    order_id: UUID
    order_item_id: UUID
    quantity: int = Field(ge=1)
    meta_data: dict = {}


class FulfillmentOrderUpdateSchema(Schema):
    order_id: UUID
    status: Optional[str] = None
    tracking_number: Optional[str] = None
    tracking_url: Optional[str] = None
    shipping_label_url: Optional[str] = None
    shipping_carrier: Optional[str] = None
    shipping_method: Optional[str] = None
    shipping_cost: Optional[Decimal] = None
    meta_data: Optional[dict] = None
    items: Optional[List[dict]] = None  # List of {order_item_id: UUID, quantity: int}


class FulfillmentSchema(Schema):
    id: UUID
    order_id: UUID
    status: str
    tracking_number: Optional[str] = None
    tracking_url: Optional[str] = None
    shipping_carrier: Optional[str] = None
    shipping_method: str = ShippingMethod.STANDARD
    shipping_label_url: Optional[str] = None
    shipping_cost: Decimal = Field(ge=0, default=Decimal("0.00"))
    notes: Optional[str] = None
    meta_data: dict = {}
    items: List[FulfillmentLineItemSchema]
    created_at: datetime
    updated_at: datetime
    date_modified: Optional[datetime] = None


class FulfillmentCreateSchema(Schema):
    order_id: UUID
    tracking_number: Optional[str] = None
    tracking_url: Optional[str] = None
    shipping_carrier: Optional[str] = None
    shipping_method: str = ShippingMethod.STANDARD
    shipping_label_url: Optional[str] = None
    shipping_cost: Decimal = Field(ge=0, default=Decimal("0.00"))
    notes: Optional[str] = None
    meta_data: dict = {}
    items: List[dict]  # List of {order_item_id: UUID, quantity: int}


class FulfillmentUpdateSchema(Schema):
    status: Optional[str] = None
    tracking_number: Optional[str] = None
    tracking_url: Optional[str] = None
    shipping_carrier: Optional[str] = None
    shipping_method: Optional[str] = None
    shipping_label_url: Optional[str] = None
    shipping_cost: Optional[Decimal] = None
    notes: Optional[str] = None
    meta_data: Optional[dict] = None
    items: Optional[List[dict]] = None  # List of {order_item_id: UUID, quantity: int}
