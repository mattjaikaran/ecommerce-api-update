from .product_admin import ProductAdmin
from .product_attribute_admin import (
    ProductAttributeAdmin,
    ProductAttributeAssignmentAdmin,
    ProductAttributeValueAdmin,
)
from .product_bundle_admin import BundleItemAdmin, ProductBundleAdmin
from .product_category_admin import ProductCategoryAdmin
from .product_review_admin import ProductReviewAdmin
from .product_tag_admin import ProductCollectionAdmin, ProductTagAdmin
from .product_variant_admin import ProductVariantAdmin

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
