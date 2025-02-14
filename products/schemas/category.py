from ninja import Schema
from datetime import datetime
from typing import Optional
from uuid import UUID


class CategorySchema(Schema):
    id: UUID
    name: str
    slug: str
    description: Optional[str] = None
    parent_id: Optional[UUID] = None
    image: Optional[str] = None
    is_active: bool = True
    position: int = 0
    seo_title: Optional[str] = None
    seo_description: Optional[str] = None
    seo_keywords: Optional[str] = None
    meta_data: dict = {}
    created_at: datetime
    updated_at: datetime


class CategoryCreateSchema(Schema):
    name: str
    slug: str
    description: Optional[str] = None
    parent_id: Optional[UUID] = None
    image: Optional[str] = None
    is_active: bool = True
    position: int = 0
    seo_title: Optional[str] = None
    seo_description: Optional[str] = None
    seo_keywords: Optional[str] = None
    meta_data: dict = {}


class CategoryUpdateSchema(Schema):
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    parent_id: Optional[UUID] = None
    image: Optional[str] = None
    seo_title: Optional[str] = None
    seo_description: Optional[str] = None
    seo_keywords: Optional[str] = None
    is_active: Optional[bool] = None
    position: Optional[int] = None
