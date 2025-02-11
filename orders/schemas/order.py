from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from ninja import Schema
from pydantic import Field, validator

from orders.models import OrderStatus, PaymentStatus, PaymentMethod, ShippingMethod
from .order_line_item import OrderLineItemSchema
from .fulfillment import FulfillmentOrderSchema
from .payment import PaymentTransactionSchema
from .refund import RefundSchema
from .tax import TaxSchema
from .note import OrderNoteSchema
from .history import OrderHistorySchema


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
    created_at: datetime
    updated_at: datetime

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
