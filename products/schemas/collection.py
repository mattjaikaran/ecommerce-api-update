from ninja import Schema
from datetime import datetime
from typing import Optional
from uuid import UUID


class CollectionSchema(Schema):
    id: UUID
    name: str
    slug: str
    description: Optional[str] = None
    image: Optional[str] = None
    is_active: bool = True
    position: int = 0
    seo_title: Optional[str] = None
    seo_description: Optional[str] = None
    seo_keywords: Optional[str] = None
    meta_data: dict = {}
    created_at: datetime
    updated_at: datetime


class CollectionCreateSchema(Schema):
    name: str
    slug: str
    description: Optional[str] = None
    image: Optional[str] = None
    is_active: bool = True
    position: int = 0
    seo_title: Optional[str] = None
    seo_description: Optional[str] = None
    seo_keywords: Optional[str] = None
    meta_data: dict = {}


class CollectionUpdateSchema(Schema):
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None
    is_active: Optional[bool] = None
    position: Optional[int] = None
    seo_title: Optional[str] = None
    seo_description: Optional[str] = None
    seo_keywords: Optional[str] = None
    meta_data: Optional[dict] = None


class CollectionProductSchema(Schema):
    id: UUID
    name: str
    slug: str
    image: Optional[str] = None
