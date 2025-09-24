from datetime import datetime
from decimal import Decimal
from uuid import UUID

from ninja import Schema


class PriceHistorySchema(Schema):
    id: UUID
    product_id: UUID
    variant_id: UUID | None
    action: str
    previous_price: Decimal
    new_price: Decimal
    reason: str | None
    notes: str | None
    created_at: datetime
    date_modified: datetime


class PriceAdjustmentSchema(Schema):
    variant_id: UUID | None
    action: str
    new_price: Decimal
    reason: str | None
    notes: str | None


class PriceAdjustmentResponseSchema(Schema):
    success: bool
    message: str
    history: PriceHistorySchema


class BulkPriceAdjustmentSchema(Schema):
    adjustments: list[PriceAdjustmentSchema]


class PriceAnalyticsSchema(Schema):
    product_id: UUID
    variant_id: UUID | None
    current_price: Decimal
    average_price: Decimal
    lowest_price: Decimal
    highest_price: Decimal
    price_changes_count: int
    last_change_date: datetime
    price_trend: str  # "increasing", "decreasing", "stable"
    competitor_price: Decimal | None
    suggested_price: Decimal | None


class PricingRuleSchema(Schema):
    id: UUID
    name: str
    description: str | None
    rule_type: str  # "markup", "margin", "fixed", "competitor_based"
    value: Decimal
    min_price: Decimal | None
    max_price: Decimal | None
    start_date: datetime | None
    end_date: datetime | None
    is_active: bool
    created_at: datetime
    date_modified: datetime
