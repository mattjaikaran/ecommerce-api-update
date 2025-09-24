from datetime import datetime
from uuid import UUID

from ninja import Schema
from pydantic import Field


class ReviewSchema(Schema):
    id: UUID
    product_id: UUID
    user_id: UUID
    rating: int = Field(ge=1, le=5)
    title: str | None = None
    comment: str
    is_verified: bool = False
    is_featured: bool = False
    meta_data: dict = {}
    created_at: datetime
    updated_at: datetime


class ReviewCreateSchema(Schema):
    product_id: UUID
    rating: int = Field(ge=1, le=5)
    title: str | None = None
    comment: str
    meta_data: dict = {}


class ReviewUpdateSchema(Schema):
    rating: int = Field(ge=1, le=5)
    title: str | None = None
    comment: str
    meta_data: dict | None = None
