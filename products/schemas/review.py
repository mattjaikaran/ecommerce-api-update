from ninja import Schema
from datetime import datetime


class ReviewSchema(Schema):
    id: str
    product_id: str
    user_id: str
    rating: int
    comment: str
    created_at: datetime
    updated_at: datetime


class ReviewCreateSchema(Schema):
    product_id: str
    user_id: str
    rating: int
    comment: str
