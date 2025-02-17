from typing import List
from ninja_extra import api_controller, http_get, http_post, http_put, http_delete
from ninja_extra.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.core.exceptions import ValidationError
from uuid import UUID
import logging

from core.cache.decorators import cached_view
from products.models import (
    Product,
    ProductVariant,
    ProductOption,
    ProductOptionValue,
    ProductVariantOption,
)
from products.schemas import (
    ProductSchema,
    ProductCreateSchema,
    ProductVariantSchema,
    ProductVariantCreateSchema,
    ProductVariantUpdateSchema,
    ProductListSchema,
    ProductUpdateSchema,
)

logger = logging.getLogger(__name__)


@api_controller("/products", tags=["Products"])
class ProductController:
    permission_classes = [IsAuthenticated]

    @http_get(
        "",
        response={
            200: List[ProductListSchema],
            400: dict,
            404: dict,
        },
    )
    @cached_view(timeout=300, key_prefix="products")
    def list_products(self):
        """
        Get all products
        """
        try:
            products = (
                Product.objects.select_related(
                    "category",
                    "created_by",
                    "updated_by",
                )
                .prefetch_related(
                    "variants",
                    "tags",
                    "collections",
                    "images",
                )
                .all()
            )
            return 200, [ProductListSchema.from_orm(product) for product in products]
        except Exception as e:
            logger.error(f"Error listing products: {e}")
            return 400, {"error": "Error listing products", "message": str(e)}

    @http_get(
        "/{id}",
        response={
            200: ProductSchema,
            400: dict,
            404: dict,
        },
        tags=["Products"],
    )
    @cached_view(timeout=300, key_prefix="product")
    def get_product(self, id: UUID):
        """
        Get a product by ID
        """
        try:
            product = (
                Product.objects.select_related(
                    "category",
                    "brand",
                )
                .prefetch_related(
                    "variants",
                    "tags",
                    "collections",
                )
                .get(id=id)
            )
            return 200, ProductSchema.from_orm(product)
        except Product.DoesNotExist:
            return 404, {"error": "Product not found"}
        except Exception as e:
            logger.error(f"Error getting product: {e}")
            return 400, {"error": "Error getting product", "message": str(e)}

    @http_post(
        "",
        response={
            201: ProductSchema,
            400: dict,
        },
        tags=["Products"],
    )
    @transaction.atomic
    def create_product(self, payload: ProductCreateSchema):
        """
        Create a new product
        """
        try:
            product = Product.objects.create(**payload.dict())
            return 201, ProductSchema.from_orm(product)
        except Exception as e:
            logger.error(f"Error creating product: {e}")
            return 400, {"error": "Error creating product", "message": str(e)}

    @http_put(
        "/{id}",
        response={
            200: ProductSchema,
            400: dict,
            404: dict,
        },
        tags=["Products"],
    )
    @transaction.atomic
    def update_product(self, id: UUID, payload: ProductUpdateSchema):
        """
        Update a product
        """
        try:
            product = get_object_or_404(Product, id=id)
            for key, value in payload.dict(exclude_unset=True).items():
                setattr(product, key, value)
            product.save()
            return 200, ProductSchema.from_orm(product)
        except Product.DoesNotExist:
            return 404, {"error": "Product not found"}
        except Exception as e:
            logger.error(f"Error updating product: {e}")
            return 400, {"error": "Error updating product", "message": str(e)}

    @http_delete(
        "/{id}",
        response={
            204: None,
            400: dict,
            404: dict,
        },
        tags=["Products"],
    )
    @transaction.atomic
    def delete_product(self, id: UUID):
        """
        Delete a product
        """
        try:
            product = get_object_or_404(Product, id=id)
            product.delete()
            return 204, None
        except Product.DoesNotExist:
            return 404, {"error": "Product not found"}
        except Exception as e:
            logger.error(f"Error deleting product: {e}")
            return 400, {"error": "Error deleting product", "message": str(e)}

    # Product Variant endpoints
    @http_get(
        "/{product_id}/variants",
        response={
            200: List[ProductVariantSchema],
            404: dict,
            500: dict,
        },
    )
    @cached_view(timeout=300, key_prefix="products")
    def list_product_variants(self, request, product_id: UUID):
        """
        Get all variants for a product
        """
        try:
            variants = ProductVariant.objects.filter(
                product_id=product_id
            ).prefetch_related(
                "options",
                "images",
            )
            return 200, [ProductVariantSchema.from_orm(variant) for variant in variants]
        except Exception as e:
            logger.error(f"Error listing variants for product {product_id}: {e}")
            return 500, {
                "error": "An error occurred while fetching product variants",
                "message": str(e),
            }

    @http_get(
        "/{product_id}/variants/{id}",
        response={
            200: ProductVariantSchema,
            404: dict,
            500: dict,
        },
    )
    @cached_view(timeout=300, key_prefix="products")
    def get_product_variant(self, request, product_id: UUID, id: UUID):
        """
        Get a product variant by ID
        """
        try:
            variant = get_object_or_404(
                ProductVariant.objects.prefetch_related(
                    "options",
                    "images",
                ),
                product_id=product_id,
                id=id,
            )
            return 200, ProductVariantSchema.from_orm(variant)
        except ProductVariant.DoesNotExist:
            return 404, {"error": "Product variant not found"}
        except Exception as e:
            logger.error(f"Error getting variant {id} for product {product_id}: {e}")
            return 500, {
                "error": "An error occurred while fetching the product variant",
                "message": str(e),
            }

    @http_post(
        "/{product_id}/variants",
        response={
            201: ProductVariantSchema,
            400: dict,
            404: dict,
            500: dict,
        },
    )
    @transaction.atomic
    def create_product_variant(
        self, request, product_id: UUID, payload: ProductVariantCreateSchema
    ):
        """
        Create a new product variant
        """
        try:
            # Ensure product exists
            product = get_object_or_404(Product, id=product_id)

            # Create variant
            variant_data = payload.dict(exclude={"options"})
            variant_data["product_id"] = product_id
            variant = ProductVariant.objects.create(**variant_data)

            # Create variant options if provided
            if hasattr(payload, "options"):
                for option in payload.options:
                    ProductVariantOption.objects.create(
                        variant=variant,
                        option_id=option.option_id,
                        value_id=option.value_id,
                    )

            return 201, ProductVariantSchema.from_orm(variant)
        except Product.DoesNotExist:
            return 404, {"error": "Product not found"}
        except ValidationError as e:
            return 400, {"error": "Validation error", "message": str(e)}
        except Exception as e:
            logger.error(f"Error creating variant for product {product_id}: {e}")
            return 500, {
                "error": "An error occurred while creating the product variant",
                "message": str(e),
            }

    @http_put(
        "/{product_id}/variants/{id}",
        response={
            200: ProductVariantSchema,
            400: dict,
            404: dict,
            500: dict,
        },
    )
    @transaction.atomic
    def update_product_variant(
        self, request, product_id: UUID, id: UUID, payload: ProductVariantUpdateSchema
    ):
        """
        Update a product variant
        """
        try:
            variant = get_object_or_404(
                ProductVariant,
                product_id=product_id,
                id=id,
            )

            # Update variant fields
            variant_data = payload.dict(exclude={"options"}, exclude_unset=True)
            for attr, value in variant_data.items():
                setattr(variant, attr, value)
            variant.save()

            # Update variant options if provided
            if "options" in payload.dict():
                # Delete existing options
                variant.options.all().delete()

                # Create new options
                for option_data in payload.options:
                    option = get_object_or_404(
                        ProductOption, id=option_data["option_id"]
                    )
                    value = get_object_or_404(
                        ProductOptionValue, id=option_data["value_id"]
                    )

                    ProductVariantOption.objects.create(
                        variant=variant,
                        option=option,
                        value=value,
                    )

            return 200, ProductVariantSchema.from_orm(variant)
        except ProductVariant.DoesNotExist:
            return 404, {"error": "Product variant not found"}
        except (ProductOption.DoesNotExist, ProductOptionValue.DoesNotExist):
            return 404, {"error": "Referenced option or value not found"}
        except ValidationError as e:
            return 400, {"error": "Validation error", "message": str(e)}
        except Exception as e:
            logger.error(f"Error updating variant {id} for product {product_id}: {e}")
            return 500, {
                "error": "An error occurred while updating the product variant",
                "message": str(e),
            }

    @http_delete(
        "/{product_id}/variants/{id}",
        response={
            204: dict,
            404: dict,
            500: dict,
        },
    )
    @transaction.atomic
    def delete_product_variant(self, request, product_id: UUID, id: UUID):
        """
        Delete a product variant
        """
        try:
            variant = get_object_or_404(
                ProductVariant,
                product_id=product_id,
                id=id,
            )
            variant.delete()
            return 204, {"message": "Product variant deleted successfully"}
        except ProductVariant.DoesNotExist:
            return 404, {"error": "Product variant not found"}
        except Exception as e:
            logger.error(f"Error deleting variant {id} for product {product_id}: {e}")
            return 500, {
                "error": "An error occurred while deleting the product variant",
                "message": str(e),
            }
