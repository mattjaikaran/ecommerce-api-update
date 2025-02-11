from ninja import Schema
from datetime import datetime
from typing import Optional


class TagSchema(Schema):
    id: str
    name: str
    slug: str
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class TagCreateSchema(Schema):
    name: str
    slug: str
    description: Optional[str] = None
