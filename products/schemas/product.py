from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from uuid import UUID
from ninja import Schema
from pydantic import Field, validator
from .product_option import ProductVariantSchema, ProductImageSchema
from .review import ReviewSchema
from .tag import TagSchema
from .collection import CollectionSchema


class ProductSchema(Schema):
    id: UUID
    name: str
    slug: str
    description: Optional[str] = None
    category_id: UUID
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
    category_id: UUID
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


class ProductListSchema(Schema):
    id: UUID
    name: str
    slug: str
    price: Decimal = Field(ge=0)
    compare_at_price: Optional[Decimal] = None
    status: str = "draft"
    featured: bool = False
    is_active: bool = True
    category_id: UUID
    thumbnail: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    @validator("thumbnail", pre=True)
    def get_thumbnail(cls, v, values):
        """Get the first image URL as thumbnail."""
        if hasattr(values.get("source"), "images"):
            images = values.get("source").images.all()
            if images:
                return images[0].image
        return None

    @validator("compare_at_price")
    def compare_at_price_must_be_greater_than_price(cls, v, values):
        if v is not None and "price" in values and v <= values["price"]:
            raise ValueError("compare_at_price must be greater than price")
        return v


class ProductUpdateSchema(Schema):
    name: str
    slug: str
    description: Optional[str] = None
    category_id: UUID
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
