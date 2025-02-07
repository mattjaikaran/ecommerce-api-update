from ninja import Schema
from datetime import datetime


class ReviewSchema(Schema):
    id: str
    product_id: str
    user_id: str
    rating: int
    comment: str
    date_created: datetime
    date_updated: datetime


class ReviewCreateSchema(Schema):
    product_id: str
    user_id: str
    rating: int
    comment: str
