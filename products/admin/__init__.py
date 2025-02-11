from .product import ProductAdmin
from .product_category import ProductCategoryAdmin
from .product_variant import ProductVariantAdmin
from .product_attribute import (
    ProductAttributeAdmin,
    ProductAttributeValueAdmin,
    ProductAttributeAssignmentAdmin,
)
from .product_bundle import ProductBundleAdmin, BundleItemAdmin
from .product_review import ProductReviewAdmin
from .product_tag import ProductTagAdmin, ProductCollectionAdmin

__all__ = [
    ProductAdmin,
    ProductCategoryAdmin,
    ProductVariantAdmin,
    ProductAttributeAdmin,
    ProductAttributeValueAdmin,
    ProductAttributeAssignmentAdmin,
    ProductBundleAdmin,
    BundleItemAdmin,
    ProductReviewAdmin,
    ProductTagAdmin,
    ProductCollectionAdmin,
]
