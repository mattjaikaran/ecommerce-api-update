from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from ninja import Schema
from pydantic import Field, validator

from orders.models import (
    OrderStatus,
    PaymentStatus,
    PaymentMethod,
    ShippingMethod,
    FulfillmentStatus,
    RefundStatus,
    TaxType,
)


class AddressSchema(Schema):
    id: str
    first_name: str
    last_name: str
    company: Optional[str] = None
    address1: str
    address2: Optional[str] = None
    city: str
    state: str
    postal_code: str
    country: str
    phone: Optional[str] = None
    email: Optional[str] = None
    is_default: bool = False


class OrderLineItemSchema(Schema):
    id: str
    product_variant_id: str
    quantity: int = Field(ge=1)
    unit_price: Decimal = Field(ge=0)
    subtotal: Decimal = Field(ge=0)
    discount_amount: Decimal = Field(ge=0)
    tax_amount: Decimal = Field(ge=0)
    total: Decimal = Field(ge=0)
    tax_rate: Decimal = Field(ge=0, le=1)
    weight: Decimal = Field(ge=0)
    meta_data: dict = {}
    date_created: datetime
    date_updated: datetime


class FulfillmentLineItemSchema(Schema):
    id: str
    fulfillment_id: str
    order_item_id: str
    quantity: int = Field(ge=1)
    meta_data: dict = {}
    date_created: datetime
    date_updated: datetime


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
    date_created: datetime
    date_updated: datetime


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


class OrderNoteSchema(Schema):
    id: str
    order_id: str
    note: str
    is_customer_visible: bool = False
    created_by_id: str
    meta_data: dict = {}
    date_created: datetime
    date_updated: datetime


class OrderHistorySchema(Schema):
    id: str
    order_id: str
    status: str
    old_status: Optional[str] = None
    notes: Optional[str] = None
    created_by_id: str
    meta_data: dict = {}
    date_created: datetime
    date_updated: datetime


class OrderSchema(Schema):
    id: str
    order_number: str
    customer_id: str
    customer_group_id: Optional[str] = None
    status: str = OrderStatus.DRAFT
    currency: str = "USD"
    subtotal: Decimal = Field(ge=0)
    shipping_amount: Decimal = Field(ge=0)
    shipping_method: str = ShippingMethod.STANDARD
    shipping_tax_amount: Decimal = Field(ge=0)
    discount_amount: Decimal = Field(ge=0)
    tax_amount: Decimal = Field(ge=0)
    total: Decimal = Field(ge=0)
    payment_status: str = PaymentStatus.PENDING
    payment_method: str = PaymentMethod.CREDIT_CARD
    payment_gateway: Optional[str] = None
    payment_gateway_id: Optional[str] = None
    payment_gateway_response: Optional[dict] = None
    billing_address_id: str
    shipping_address_id: str
    email: str
    phone: Optional[str] = None
    customer_note: Optional[str] = None
    staff_notes: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    meta_data: dict = {}
    items: List[OrderLineItemSchema]
    fulfillments: List[FulfillmentOrderSchema]
    transactions: List[PaymentTransactionSchema]
    refunds: List[RefundSchema]
    taxes: List[TaxSchema]
    notes: List[OrderNoteSchema]
    history: List[OrderHistorySchema]
    date_created: datetime
    date_updated: datetime

    @validator("total")
    def validate_total(cls, v, values):
        if "subtotal" in values and v < values["subtotal"]:
            raise ValueError("Total cannot be less than subtotal")
        return v


class OrderCreateSchema(Schema):
    customer_id: str
    customer_group_id: Optional[str] = None
    currency: str = "USD"
    shipping_method: str = ShippingMethod.STANDARD
    payment_method: str = PaymentMethod.CREDIT_CARD
    payment_gateway: Optional[str] = None
    billing_address_id: str
    shipping_address_id: str
    email: str
    phone: Optional[str] = None
    customer_note: Optional[str] = None
    meta_data: dict = {}
    items: List[dict]  # List of {product_variant_id: str, quantity: int}


class OrderUpdateSchema(Schema):
    status: Optional[str] = None
    shipping_method: Optional[str] = None
    payment_method: Optional[str] = None
    payment_gateway: Optional[str] = None
    billing_address_id: Optional[str] = None
    shipping_address_id: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    customer_note: Optional[str] = None
    staff_notes: Optional[str] = None
    meta_data: Optional[dict] = None


class OrderLineItemCreateSchema(Schema):
    product_variant_id: str
    quantity: int = Field(ge=1)


class OrderLineItemUpdateSchema(Schema):
    quantity: int = Field(ge=1)


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


class OrderNoteCreateSchema(Schema):
    order_id: str
    note: str
    is_customer_visible: bool = False
    meta_data: dict = {}
