from .product import ProductSchema, ProductCreateSchema
from .category import CategorySchema, CategoryCreateSchema
from .collection import CollectionSchema, CollectionCreateSchema
from .review import ReviewSchema, ReviewCreateSchema
from .tag import TagSchema, TagCreateSchema
from .product_option import (
    ProductOptionSchema,
    ProductVariantSchema,
    ProductImageSchema,
)

all = [
    ProductSchema,
    ProductCreateSchema,
    CategorySchema,
    CategoryCreateSchema,
    CollectionSchema,
    CollectionCreateSchema,
    ReviewSchema,
    ReviewCreateSchema,
    TagSchema,
    TagCreateSchema,
    ProductOptionSchema,
    ProductVariantSchema,
    ProductImageSchema,
]
