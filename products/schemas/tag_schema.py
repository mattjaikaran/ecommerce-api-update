from datetime import datetime
from uuid import UUID

from ninja import Schema


class TagSchema(Schema):
    id: UUID
    name: str
    slug: str
    description: str | None = None
    meta_data: dict = {}
    created_at: datetime
    updated_at: datetime


class TagCreateSchema(Schema):
    name: str
    slug: str
    description: str | None = None
    meta_data: dict = {}


class TagUpdateSchema(Schema):
    name: str | None = None
    slug: str | None = None
    description: str | None = None
    meta_data: dict | None = None
