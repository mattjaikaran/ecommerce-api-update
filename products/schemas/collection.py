from ninja import Schema
from datetime import datetime
from typing import Optional


class CollectionSchema(Schema):
    id: str
    name: str
    slug: str
    description: Optional[str] = None
    image: Optional[str] = None
    is_active: bool = True
    position: int = 0
    seo_title: Optional[str] = None
    seo_description: Optional[str] = None
    seo_keywords: Optional[str] = None
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
