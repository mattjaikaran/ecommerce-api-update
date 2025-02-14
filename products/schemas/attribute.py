from typing import Optional, List
from uuid import UUID
from datetime import datetime
from ninja import Schema


class AttributeValueSchema(Schema):
    id: UUID
    attribute_id: UUID
    value: str
    position: int = 0
    meta_data: dict = {}
    created_at: datetime
    updated_at: datetime
    date_modified: Optional[datetime] = None


class AttributeValueCreateSchema(Schema):
    value: str
    position: int = 0
    meta_data: dict = {}


class AttributeValueUpdateSchema(Schema):
    value: Optional[str] = None
    position: Optional[int] = None
    meta_data: Optional[dict] = None


class AttributeSchema(Schema):
    id: UUID
    name: str
    code: str
    description: Optional[str] = None
    is_filterable: bool = True
    position: int = 0
    values: List[AttributeValueSchema] = []
    meta_data: dict = {}
    created_at: datetime
    updated_at: datetime
    date_modified: Optional[datetime] = None


class AttributeCreateSchema(Schema):
    name: str
    code: str
    description: Optional[str] = None
    is_filterable: bool = True
    position: int = 0
    meta_data: dict = {}


class AttributeUpdateSchema(Schema):
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None
    is_filterable: Optional[bool] = None
    position: Optional[int] = None
    meta_data: Optional[dict] = None


class AttributeGroupSchema(Schema):
    id: UUID
    name: str
    description: Optional[str] = None
    position: int = 0
    meta_data: dict = {}
    created_at: datetime
    updated_at: datetime
    date_modified: Optional[datetime] = None


class AttributeGroupCreateSchema(Schema):
    name: str
    description: Optional[str] = None
    position: int = 0
    meta_data: dict = {}


class AttributeGroupUpdateSchema(Schema):
    name: Optional[str] = None
    description: Optional[str] = None
    position: Optional[int] = None
    meta_data: Optional[dict] = None


class AttributeAssignmentSchema(Schema):
    id: UUID
    product_id: UUID
    attribute_id: UUID
    value_id: UUID
    meta_data: dict = {}
    created_at: datetime
    updated_at: datetime
    date_modified: Optional[datetime] = None


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
    description: Optional[str]
    created_at: datetime
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
    created_at: datetime
    date_modified: datetime


class ProductAttributeGroupCreateSchema(Schema):
    name: str
    description: Optional[str]
    position: int = 0
    attribute_ids: list[UUID]
