from datetime import datetime
from uuid import UUID

from ninja import Schema


class AttributeValueSchema(Schema):
    id: UUID
    attribute_id: UUID
    value: str
    position: int = 0
    meta_data: dict = {}
    created_at: datetime
    updated_at: datetime
    date_modified: datetime | None = None


class AttributeValueCreateSchema(Schema):
    value: str
    position: int = 0
    meta_data: dict = {}


class AttributeValueUpdateSchema(Schema):
    value: str | None = None
    position: int | None = None
    meta_data: dict | None = None


class AttributeSchema(Schema):
    id: UUID
    name: str
    code: str
    description: str | None = None
    is_filterable: bool = True
    position: int = 0
    values: list[AttributeValueSchema] = []
    meta_data: dict = {}
    created_at: datetime
    updated_at: datetime
    date_modified: datetime | None = None


class AttributeCreateSchema(Schema):
    name: str
    code: str
    description: str | None = None
    is_filterable: bool = True
    position: int = 0
    meta_data: dict = {}


class AttributeUpdateSchema(Schema):
    name: str | None = None
    code: str | None = None
    description: str | None = None
    is_filterable: bool | None = None
    position: int | None = None
    meta_data: dict | None = None


class AttributeGroupSchema(Schema):
    id: UUID
    name: str
    description: str | None = None
    position: int = 0
    meta_data: dict = {}
    created_at: datetime
    updated_at: datetime
    date_modified: datetime | None = None


class AttributeGroupCreateSchema(Schema):
    name: str
    description: str | None = None
    position: int = 0
    meta_data: dict = {}


class AttributeGroupUpdateSchema(Schema):
    name: str | None = None
    description: str | None = None
    position: int | None = None
    meta_data: dict | None = None


class AttributeAssignmentSchema(Schema):
    id: UUID
    product_id: UUID
    attribute_id: UUID
    value_id: UUID
    meta_data: dict = {}
    created_at: datetime
    updated_at: datetime
    date_modified: datetime | None = None


class AttributeAssignmentCreateSchema(Schema):
    product_id: UUID
    attribute_id: UUID
    value_id: UUID
    meta_data: dict = {}


class AttributeFilterSchema(Schema):
    attribute_id: UUID
    attribute_name: str
    attribute_code: str
    values: list[AttributeValueSchema]
    selected_values: list[UUID]


class AttributeGroupProductSchema(Schema):
    id: UUID
    name: str
    slug: str
    description: str | None
    created_at: datetime
    date_modified: datetime


class AttributeGroupProductCreateSchema(Schema):
    product_ids: list[UUID]


class AttributeGroupProductUpdateSchema(Schema):
    product_ids: list[UUID] | None


class ProductAttributeGroupSchema(Schema):
    id: UUID
    name: str
    description: str | None
    position: int
    attributes: list[AttributeSchema]
    created_at: datetime
    date_modified: datetime


class ProductAttributeGroupCreateSchema(Schema):
    name: str
    description: str | None
    position: int = 0
    attribute_ids: list[UUID]
