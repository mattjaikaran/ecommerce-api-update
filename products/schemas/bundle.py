from typing import Optional, List
from uuid import UUID
from datetime import datetime
from decimal import Decimal
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
    date_modified: Optional[datetime] = None


class BundleItemCreateSchema(BundleItemBaseSchema):
    meta_data: dict = {}


class BundleItemUpdateSchema(Schema):
    product_id: Optional[UUID] = None
    quantity: Optional[int] = None
    position: Optional[int] = None
    meta_data: Optional[dict] = None


class BundleBaseSchema(Schema):
    name: str
    slug: str
    description: Optional[str] = None
    discount_percentage: Decimal = Field(ge=0, le=100)
    is_active: bool = True
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class BundleSchema(Schema):
    id: UUID
    name: str
    slug: str
    description: Optional[str] = None
    discount_percentage: Decimal = Field(ge=0, le=100)
    total_price: Decimal = Field(ge=0)
    discounted_price: Decimal = Field(ge=0)
    is_active: bool = True
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    meta_data: dict = {}
    items: List[BundleItemSchema] = []
    created_at: datetime
    updated_at: datetime
    date_modified: Optional[datetime] = None


class BundleCreateSchema(Schema):
    name: str
    slug: str
    description: Optional[str] = None
    discount_percentage: Decimal = Field(ge=0, le=100)
    is_active: bool = True
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    meta_data: dict = {}
    items: List[dict] = []  # List of {product_id: UUID, quantity: int, position: int}


class BundleUpdateSchema(Schema):
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    discount_percentage: Optional[Decimal] = None
    is_active: Optional[bool] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    meta_data: Optional[dict] = None
    items: Optional[List[dict]] = (
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
