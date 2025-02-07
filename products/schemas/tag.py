from ninja import Schema
from datetime import datetime
from typing import Optional


class TagSchema(Schema):
    id: str
    name: str
    slug: str
    description: Optional[str] = None
    date_created: datetime
    date_updated: datetime


class TagCreateSchema(Schema):
    name: str
    slug: str
    description: Optional[str] = None
