from ninja import Schema
from uuid import UUID


class UserSchema(Schema):
    id: UUID
    username: str
    email: str
    first_name: str
    last_name: str


class UserSignupSchema(Schema):
    username: str
    email: str
    password: str
    first_name: str
    last_name: str


class UserLoginSchema(Schema):
    username: str
    password: str


class UserLogoutSchema(Schema):
    message: str


class UserUpdateSchema(Schema):
    username: str
    email: str
    first_name: str
    last_name: str


class UserDeleteSchema(Schema):
    message: str
