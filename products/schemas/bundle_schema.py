from datetime import datetime
from decimal import Decimal
from uuid import UUID

from ninja import Schema
from pydantic import Field


class BundleItemBaseSchema(Schema):
    product_id: UUID
    quantity: int = 1
    position: int = 0


class BundleItemSchema(Schema):
    id: UUID
    bundle_id: UUID
    product_id: UUID
    quantity: int = Field(ge=1)
    position: int = 0
    meta_data: dict = {}
    created_at: datetime
    updated_at: datetime
    date_modified: datetime | None = None


class BundleItemCreateSchema(BundleItemBaseSchema):
    meta_data: dict = {}


class BundleItemUpdateSchema(Schema):
    product_id: UUID | None = None
    quantity: int | None = None
    position: int | None = None
    meta_data: dict | None = None


class BundleBaseSchema(Schema):
    name: str
    slug: str
    description: str | None = None
    discount_percentage: Decimal = Field(ge=0, le=100)
    is_active: bool = True
    start_date: datetime | None = None
    end_date: datetime | None = None


class BundleSchema(Schema):
    id: UUID
    name: str
    slug: str
    description: str | None = None
    discount_percentage: Decimal = Field(ge=0, le=100)
    total_price: Decimal = Field(ge=0)
    discounted_price: Decimal = Field(ge=0)
    is_active: bool = True
    start_date: datetime | None = None
    end_date: datetime | None = None
    meta_data: dict = {}
    items: list[BundleItemSchema] = []
    created_at: datetime
    updated_at: datetime
    date_modified: datetime | None = None


class BundleCreateSchema(Schema):
    name: str
    slug: str
    description: str | None = None
    discount_percentage: Decimal = Field(ge=0, le=100)
    is_active: bool = True
    start_date: datetime | None = None
    end_date: datetime | None = None
    meta_data: dict = {}
    items: list[dict] = []  # List of {product_id: UUID, quantity: int, position: int}


class BundleUpdateSchema(Schema):
    name: str | None = None
    slug: str | None = None
    description: str | None = None
    discount_percentage: Decimal | None = None
    is_active: bool | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    meta_data: dict | None = None
    items: list[dict] | None = (
        None  # List of {product_id: UUID, quantity: int, position: int}
    )


class BundleAnalyticsSchema(Schema):
    id: UUID
    name: str
    total_sales: int
    total_revenue: Decimal
    average_order_value: Decimal
    conversion_rate: Decimal
    views: int
    start_date: datetime
    end_date: datetime | None
    is_active: bool


class BundleSearchSchema(Schema):
    id: UUID
    name: str
    slug: str
    description: str | None
    discount_percentage: Decimal
    total_price: Decimal
    discounted_price: Decimal
    product_count: int
    is_active: bool
    start_date: datetime | None
    end_date: datetime | None
    relevance_score: float
