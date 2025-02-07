from ninja import Schema
from datetime import datetime
from core.schemas import UserSchema


class FeedbackSchema(Schema):
    id: int
    user: UserSchema
    feedback: str
    created_at: datetime
    updated_at: datetime


class FeedbackCreateSchema(Schema):
    feedback: str
