from datetime import datetime
from typing import Optional, List
from ninja import Schema
from pydantic import Field

from orders.models import ShippingMethod


class FulfillmentLineItemSchema(Schema):
    id: str
    fulfillment_id: str
    order_item_id: str
    quantity: int = Field(ge=1)
    meta_data: dict = {}
    created_at: datetime
    updated_at: datetime


class FulfillmentOrderSchema(Schema):
    id: str
    order_id: str
    status: str
    tracking_number: Optional[str] = None
    tracking_url: Optional[str] = None
    shipping_carrier: Optional[str] = None
    shipping_method: str = ShippingMethod.STANDARD
    shipping_label_url: Optional[str] = None
    notes: Optional[str] = None
    meta_data: dict = {}
    items: List[FulfillmentLineItemSchema]
    created_at: datetime
    updated_at: datetime


class FulfillmentOrderCreateSchema(Schema):
    order_id: str
    tracking_number: Optional[str] = None
    tracking_url: Optional[str] = None
    shipping_carrier: Optional[str] = None
    shipping_method: str = ShippingMethod.STANDARD
    shipping_label_url: Optional[str] = None
    notes: Optional[str] = None
    meta_data: dict = {}
    items: List[dict]  # List of {order_item_id: str, quantity: int}


class FulfillmentOrderUpdateSchema(Schema):
    status: Optional[str] = None
    tracking_number: Optional[str] = None
    tracking_url: Optional[str] = None
    shipping_carrier: Optional[str] = None
    shipping_method: Optional[str] = None
    shipping_label_url: Optional[str] = None
    notes: Optional[str] = None
    meta_data: Optional[dict] = None
