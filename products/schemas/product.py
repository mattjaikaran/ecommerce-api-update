from ninja import Schema


class ProductSchema(Schema):
    name: str
    description: str
    price: float
    stock: int
    is_active: bool


class ProductVariantSchema(Schema):
    name: str
    description: str
    price: float
    stock: int
    is_active: bool


class ProductOptionSchema(Schema):
    name: str
    description: str
    price: float
    stock: int
    is_active: bool


class ProductImageSchema(Schema):
    url: str
    alt_text: str
    position: int


class CategorySchema(Schema):
    name: str
    description: str
    parent_id: int
    is_active: bool


class CollectionSchema(Schema):
    name: str
    description: str
    products: list[ProductSchema]
    is_active: bool


class ProductReviewSchema(Schema):
    product_id: int
    user_id: int
    rating: int
    comment: str


class ProductTagSchema(Schema):
    product_id: int
    name: str
    description: str


class ProductCollectionSchema(Schema):
    name: str
    description: str
    products: list[ProductSchema]
    is_active: bool
