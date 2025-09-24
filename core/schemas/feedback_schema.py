from datetime import datetime
from uuid import UUID

from ninja import Schema


class CustomerFeedbackSchema(Schema):
    id: UUID
    customer: "UserSchema"
    feedback: str
    rating: int
    created_at: datetime
    updated_at: datetime


class CustomerFeedbackCreateSchema(Schema):
    customer_id: UUID
    feedback: str
    rating: int
