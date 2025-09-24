from datetime import datetime
from uuid import UUID

from ninja import Schema


class CategorySchema(Schema):
    id: UUID
    name: str
    slug: str
    description: str | None = None
    parent_id: UUID | None = None
    image: str | None = None
    is_active: bool = True
    position: int = 0
    seo_title: str | None = None
    seo_description: str | None = None
    seo_keywords: str | None = None
    meta_data: dict = {}
    created_at: datetime
    updated_at: datetime


class CategoryCreateSchema(Schema):
    name: str
    slug: str
    description: str | None = None
    parent_id: UUID | None = None
    image: str | None = None
    is_active: bool = True
    position: int = 0
    seo_title: str | None = None
    seo_description: str | None = None
    seo_keywords: str | None = None
    meta_data: dict = {}


class CategoryUpdateSchema(Schema):
    name: str | None = None
    slug: str | None = None
    description: str | None = None
    parent_id: UUID | None = None
    image: str | None = None
    seo_title: str | None = None
    seo_description: str | None = None
    seo_keywords: str | None = None
    is_active: bool | None = None
    position: int | None = None
