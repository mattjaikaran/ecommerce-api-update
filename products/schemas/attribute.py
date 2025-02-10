from typing import Optional
from uuid import UUID
from datetime import datetime
from ninja import Schema


class AttributeSchema(Schema):
    id: UUID
    name: str
    code: str
    description: Optional[str]
    is_filterable: bool
    position: int
    date_created: datetime
    date_modified: datetime


class AttributeCreateSchema(Schema):
    name: str
    code: str
    description: Optional[str]
    is_filterable: bool = True
    position: int = 0


class AttributeUpdateSchema(Schema):
    name: Optional[str]
    code: Optional[str]
    description: Optional[str]
    is_filterable: Optional[bool]
    position: Optional[int]


class AttributeValueSchema(Schema):
    id: UUID
    attribute_id: UUID
    value: str
    position: int
    date_created: datetime
    date_modified: datetime


class AttributeValueCreateSchema(Schema):
    value: str
    position: int = 0


class AttributeValueUpdateSchema(Schema):
    value: Optional[str]
    position: Optional[int]


class AttributeAssignmentSchema(Schema):
    id: UUID
    product_id: UUID
    attribute_id: UUID
    value_id: UUID
    date_created: datetime
    date_modified: datetime


class AttributeAssignmentCreateSchema(Schema):
    attribute_id: UUID
    value_id: UUID


class AttributeFilterSchema(Schema):
    attribute_id: UUID
    attribute_name: str
    attribute_code: str
    values: list[AttributeValueSchema]
    selected_values: list[UUID]


class AttributeGroupSchema(Schema):
    id: UUID
    name: str
    description: Optional[str]
    position: int
    attributes: list[AttributeSchema]
    date_created: datetime
    date_modified: datetime


class AttributeGroupCreateSchema(Schema):
    name: str
    description: Optional[str]
    position: int = 0
    attribute_ids: list[UUID]


class AttributeGroupUpdateSchema(Schema):
    name: Optional[str]
    description: Optional[str]
    position: Optional[int]
    attribute_ids: Optional[list[UUID]]


class AttributeGroupProductSchema(Schema):
    id: UUID
    name: str
    slug: str
    description: Optional[str]
    date_created: datetime
    date_modified: datetime


class AttributeGroupProductCreateSchema(Schema):
    product_ids: list[UUID]


class AttributeGroupProductUpdateSchema(Schema):
    product_ids: Optional[list[UUID]]


class ProductAttributeGroupSchema(Schema):
    id: UUID
    name: str
    description: Optional[str]
    position: int
    attributes: list[AttributeSchema]
    date_created: datetime
    date_modified: datetime


class ProductAttributeGroupCreateSchema(Schema):
    name: str
    description: Optional[str]
    position: int = 0
    attribute_ids: list[UUID]
