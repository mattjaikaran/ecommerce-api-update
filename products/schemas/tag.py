from ninja import Schema
from datetime import datetime
from typing import Optional
from uuid import UUID


class TagSchema(Schema):
    id: UUID
    name: str
    slug: str
    description: Optional[str] = None
    meta_data: dict = {}
    created_at: datetime
    updated_at: datetime


class TagCreateSchema(Schema):
    name: str
    slug: str
    description: Optional[str] = None
    meta_data: dict = {}


class TagUpdateSchema(Schema):
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    meta_data: Optional[dict] = None
