from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from ninja import Schema
from pydantic import Field, validator


class ProductCategorySchema(Schema):
    id: str
    name: str
    slug: str
    description: Optional[str] = None
    parent_id: Optional[str] = None
    image: Optional[str] = None
    seo_title: Optional[str] = None
    seo_description: Optional[str] = None
    seo_keywords: Optional[str] = None
    is_active: bool = True
    position: int = 0
    date_created: datetime
    date_updated: datetime


class ProductOptionValueSchema(Schema):
    id: str
    name: str
    position: int = 0
    date_created: datetime
    date_updated: datetime


class ProductOptionSchema(Schema):
    id: str
    name: str
    position: int = 0
    values: List[ProductOptionValueSchema]
    date_created: datetime
    date_updated: datetime


class ProductVariantOptionSchema(Schema):
    id: str
    option_id: str
    value_id: str
    date_created: datetime
    date_updated: datetime


class ProductImageSchema(Schema):
    id: str
    product_id: str
    variant_id: Optional[str] = None
    image: str
    alt_text: Optional[str] = None
    position: int = 0
    date_created: datetime
    date_updated: datetime


class ProductReviewSchema(Schema):
    id: str
    product_id: str
    user_id: str
    rating: int = Field(ge=1, le=5)
    title: str
    comment: str
    is_verified: bool = False
    is_featured: bool = False
    date_created: datetime
    date_updated: datetime


class ProductTagSchema(Schema):
    id: str
    name: str
    slug: str
    description: Optional[str] = None
    date_created: datetime
    date_updated: datetime


class ProductCollectionSchema(Schema):
    id: str
    name: str
    slug: str
    description: Optional[str] = None
    image: Optional[str] = None
    is_active: bool = True
    position: int = 0
    seo_title: Optional[str] = None
    seo_description: Optional[str] = None
    seo_keywords: Optional[str] = None
    date_created: datetime
    date_updated: datetime


class ProductVariantSchema(Schema):
    id: str
    product_id: str
    name: str
    sku: str
    barcode: Optional[str] = None
    price: Decimal = Field(ge=0)
    compare_at_price: Optional[Decimal] = None
    cost_price: Optional[Decimal] = None
    inventory_quantity: int = 0
    low_stock_threshold: int = 10
    weight: Optional[Decimal] = None
    length: Optional[Decimal] = None
    width: Optional[Decimal] = None
    height: Optional[Decimal] = None
    position: int = 0
    is_active: bool = True
    meta_data: dict = {}
    options: List[ProductVariantOptionSchema]
    images: List[ProductImageSchema]
    date_created: datetime
    date_updated: datetime

    @validator("compare_at_price")
    def compare_at_price_must_be_greater_than_price(cls, v, values):
        if v is not None and "price" in values and v <= values["price"]:
            raise ValueError("compare_at_price must be greater than price")
        return v


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
    reviews: List[ProductReviewSchema]
    tags: List[ProductTagSchema]
    collections: List[ProductCollectionSchema]
    date_created: datetime
    date_updated: datetime

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


class ProductUpdateSchema(ProductCreateSchema):
    pass


class ProductVariantCreateSchema(Schema):
    product_id: str
    name: str
    sku: str
    barcode: Optional[str] = None
    price: Decimal = Field(ge=0)
    compare_at_price: Optional[Decimal] = None
    cost_price: Optional[Decimal] = None
    inventory_quantity: int = 0
    low_stock_threshold: int = 10
    weight: Optional[Decimal] = None
    length: Optional[Decimal] = None
    width: Optional[Decimal] = None
    height: Optional[Decimal] = None
    position: int = 0
    is_active: bool = True
    meta_data: dict = {}
    options: List[dict]


class ProductVariantUpdateSchema(ProductVariantCreateSchema):
    pass


class ProductCategoryCreateSchema(Schema):
    name: str
    slug: str
    description: Optional[str] = None
    parent_id: Optional[str] = None
    image: Optional[str] = None
    seo_title: Optional[str] = None
    seo_description: Optional[str] = None
    seo_keywords: Optional[str] = None
    is_active: bool = True
    position: int = 0


class ProductCategoryUpdateSchema(ProductCategoryCreateSchema):
    pass


class ProductOptionCreateSchema(Schema):
    name: str
    position: int = 0
    values: List[str]


class ProductOptionUpdateSchema(ProductOptionCreateSchema):
    pass


class ProductReviewCreateSchema(Schema):
    product_id: str
    rating: int = Field(ge=1, le=5)
    title: str
    comment: str


class ProductReviewUpdateSchema(ProductReviewCreateSchema):
    pass


class ProductTagCreateSchema(Schema):
    name: str
    slug: str
    description: Optional[str] = None


class ProductTagUpdateSchema(ProductTagCreateSchema):
    pass


class ProductCollectionCreateSchema(Schema):
    name: str
    slug: str
    description: Optional[str] = None
    image: Optional[str] = None
    is_active: bool = True
    position: int = 0
    seo_title: Optional[str] = None
    seo_description: Optional[str] = None
    seo_keywords: Optional[str] = None


class ProductCollectionUpdateSchema(ProductCollectionCreateSchema):
    pass
