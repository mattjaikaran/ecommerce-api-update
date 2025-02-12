from ninja import Schema
from datetime import datetime
from uuid import UUID


class ReviewSchema(Schema):
    id: UUID
    product_id: UUID
    user_id: UUID
    rating: int
    comment: str
    created_at: datetime
    updated_at: datetime


class ReviewCreateSchema(Schema):
    product_id: UUID
    user_id: UUID
    rating: int
    comment: str
