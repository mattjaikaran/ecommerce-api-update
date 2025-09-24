from datetime import datetime
from uuid import UUID

from ninja import Schema


class CollectionSchema(Schema):
    id: UUID
    name: str
    slug: str
    description: str | None = None
    image: str | None = None
    is_active: bool = True
    position: int = 0
    seo_title: str | None = None
    seo_description: str | None = None
    seo_keywords: str | None = None
    meta_data: dict = {}
    created_at: datetime
    updated_at: datetime


class CollectionCreateSchema(Schema):
    name: str
    slug: str
    description: str | None = None
    image: str | None = None
    is_active: bool = True
    position: int = 0
    seo_title: str | None = None
    seo_description: str | None = None
    seo_keywords: str | None = None
    meta_data: dict = {}


class CollectionUpdateSchema(Schema):
    name: str | None = None
    slug: str | None = None
    description: str | None = None
    image: str | None = None
    is_active: bool | None = None
    position: int | None = None
    seo_title: str | None = None
    seo_description: str | None = None
    seo_keywords: str | None = None
    meta_data: dict | None = None


class CollectionProductSchema(Schema):
    id: UUID
    name: str
    slug: str
    image: str | None = None
