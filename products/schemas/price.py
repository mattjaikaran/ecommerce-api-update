from typing import Optional
from uuid import UUID
from datetime import datetime
from decimal import Decimal
from ninja import Schema


class PriceHistorySchema(Schema):
    id: UUID
    product_id: UUID
    variant_id: Optional[UUID]
    action: str
    previous_price: Decimal
    new_price: Decimal
    reason: Optional[str]
    notes: Optional[str]
    date_created: datetime
    date_modified: datetime


class PriceAdjustmentSchema(Schema):
    variant_id: Optional[UUID]
    action: str
    new_price: Decimal
    reason: Optional[str]
    notes: Optional[str]


class PriceAdjustmentResponseSchema(Schema):
    success: bool
    message: str
    history: PriceHistorySchema


class BulkPriceAdjustmentSchema(Schema):
    adjustments: list[PriceAdjustmentSchema]


class PriceAnalyticsSchema(Schema):
    product_id: UUID
    variant_id: Optional[UUID]
    current_price: Decimal
    average_price: Decimal
    lowest_price: Decimal
    highest_price: Decimal
    price_changes_count: int
    last_change_date: datetime
    price_trend: str  # "increasing", "decreasing", "stable"
    competitor_price: Optional[Decimal]
    suggested_price: Optional[Decimal]


class PricingRuleSchema(Schema):
    id: UUID
    name: str
    description: Optional[str]
    rule_type: str  # "markup", "margin", "fixed", "competitor_based"
    value: Decimal
    min_price: Optional[Decimal]
    max_price: Optional[Decimal]
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    is_active: bool
    date_created: datetime
    date_modified: datetime
