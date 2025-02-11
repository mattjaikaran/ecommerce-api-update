from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from ninja import Schema
from pydantic import Field, validator
from .product_option import ProductVariantSchema, ProductImageSchema
from .review import ReviewSchema
from .tag import TagSchema
from .collection import CollectionSchema


class ProductSchema(Schema):
    id: str
    name: str
    slug: str
    description: Optional[str] = None
    category_id: str
    type: str = "physical"
    tax_class: str = "standard"
    shipping_class: str = "standard"
    price: Decimal = Field(ge=0)
    compare_at_price: Optional[Decimal] = None
    cost_price: Optional[Decimal] = None
    quantity: int = 0
    low_stock_threshold: int = 10
    weight: Optional[Decimal] = None
    length: Optional[Decimal] = None
    width: Optional[Decimal] = None
    height: Optional[Decimal] = None
    digital_file: Optional[str] = None
    download_limit: Optional[int] = None
    is_active: bool = True
    status: str = "draft"
    featured: bool = False
    seo_title: Optional[str] = None
    seo_description: Optional[str] = None
    seo_keywords: Optional[str] = None
    meta_data: dict = {}
    variants: List[ProductVariantSchema]
    images: List[ProductImageSchema]
    reviews: List[ReviewSchema]
    tags: List[TagSchema]
    collections: List[CollectionSchema]
    created_at: datetime
    updated_at: datetime

    @validator("compare_at_price")
    def compare_at_price_must_be_greater_than_price(cls, v, values):
        if v is not None and "price" in values and v <= values["price"]:
            raise ValueError("compare_at_price must be greater than price")
        return v


class ProductCreateSchema(Schema):
    name: str
    slug: str
    description: Optional[str] = None
    category_id: str
    type: str = "physical"
    tax_class: str = "standard"
    shipping_class: str = "standard"
    price: Decimal = Field(ge=0)
    compare_at_price: Optional[Decimal] = None
    cost_price: Optional[Decimal] = None
    quantity: int = 0
    low_stock_threshold: int = 10
    weight: Optional[Decimal] = None
    length: Optional[Decimal] = None
    width: Optional[Decimal] = None
    height: Optional[Decimal] = None
    digital_file: Optional[str] = None
    download_limit: Optional[int] = None
    is_active: bool = True
    status: str = "draft"
    featured: bool = False
    seo_title: Optional[str] = None
    seo_description: Optional[str] = None
    seo_keywords: Optional[str] = None
    meta_data: dict = {}
