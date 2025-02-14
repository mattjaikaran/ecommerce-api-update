from datetime import datetime
from typing import Optional
from ninja import Schema
from uuid import UUID
from .users import UserSchema


class CustomerSchema(Schema):
    id: UUID
    user: UserSchema
    phone: Optional[str] = None
    customer_group_id: Optional[UUID] = None
    meta_data: dict = {}
    is_default: bool = False
    is_active: bool = True
    is_deleted: bool = False
    deleted_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


class CustomerCreateSchema(Schema):
    user_id: UUID
    phone: Optional[str] = None
    customer_group_id: Optional[UUID] = None
    meta_data: dict = {}
    is_default: bool = False


class CustomerUpdateSchema(Schema):
    phone: Optional[str] = None
    customer_group_id: Optional[UUID] = None
    meta_data: Optional[dict] = None
    is_default: Optional[bool] = None
