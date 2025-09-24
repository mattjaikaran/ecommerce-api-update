from datetime import datetime

from ninja import Schema


class AddressSchema(Schema):
    id: int
    user: "UserSchema"
    address_line_1: str
    address_line_2: str
    city: str
    state: str
    zip_code: str
    country: str
    is_default: bool
    created_at: datetime
    updated_at: datetime


class AddressCreateSchema(Schema):
    address_line_1: str
    address_line_2: str
    city: str
    state: str
    zip_code: str
    country: str
    is_default: bool
