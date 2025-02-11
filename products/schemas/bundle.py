from typing import Optional, List
from uuid import UUID
from datetime import datetime
from decimal import Decimal
from ninja import Schema


class BundleItemBaseSchema(Schema):
    product_id: UUID
    quantity: int = 1
    position: int = 0


class BundleItemSchema(BundleItemBaseSchema):
    id: UUID
    bundle_id: UUID
    created_at: datetime
    date_modified: datetime


class BundleItemCreateSchema(BundleItemBaseSchema):
    pass


class BundleItemUpdateSchema(Schema):
    product_id: Optional[UUID]
    quantity: Optional[int]
    position: Optional[int]


class BundleBaseSchema(Schema):
    name: str
    slug: str
    description: Optional[str]
    discount_percentage: Decimal
    is_active: bool = True
    start_date: Optional[datetime]
    end_date: Optional[datetime]


class BundleSchema(BundleBaseSchema):
    id: UUID
    items: List[BundleItemSchema]
    created_at: datetime
    date_modified: datetime
    total_price: Decimal
    discounted_price: Decimal


class BundleCreateSchema(BundleBaseSchema):
    items: List[BundleItemCreateSchema]


class BundleUpdateSchema(Schema):
    name: Optional[str]
    slug: Optional[str]
    description: Optional[str]
    discount_percentage: Optional[Decimal]
    is_active: Optional[bool]
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    items: Optional[List[BundleItemCreateSchema]]


class BundleAnalyticsSchema(Schema):
    id: UUID
    name: str
    total_sales: int
    total_revenue: Decimal
    average_order_value: Decimal
    conversion_rate: Decimal
    views: int
    start_date: datetime
    end_date: Optional[datetime]
    is_active: bool


class BundleSearchSchema(Schema):
    id: UUID
    name: str
    slug: str
    description: Optional[str]
    discount_percentage: Decimal
    total_price: Decimal
    discounted_price: Decimal
    product_count: int
    is_active: bool
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    relevance_score: float
