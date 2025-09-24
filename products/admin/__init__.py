from .product import ProductAdmin
from .product_attribute import (
    ProductAttributeAdmin,
    ProductAttributeAssignmentAdmin,
    ProductAttributeValueAdmin,
)
from .product_bundle import BundleItemAdmin, ProductBundleAdmin
from .product_category import ProductCategoryAdmin
from .product_review import ProductReviewAdmin
from .product_tag import ProductCollectionAdmin, ProductTagAdmin
from .product_variant import ProductVariantAdmin

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
