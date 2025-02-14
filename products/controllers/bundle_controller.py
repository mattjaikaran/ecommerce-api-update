from typing import List
from uuid import UUID
from ninja_extra import api_controller, http_get, http_post, http_put, http_delete
from ninja_extra.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import transaction
from ..models import Product, ProductBundle, BundleItem
from ..schemas.bundle import (
    BundleSchema,
    BundleCreateSchema,
    BundleUpdateSchema,
    BundleItemSchema,
    BundleItemCreateSchema,
    BundleItemUpdateSchema,
)
import logging

logger = logging.getLogger(__name__)


@api_controller("/products/bundles", tags=["Product Bundles"])
class BundleController:
    permission_classes = [IsAuthenticated]

    @http_get("", response={200: List[BundleSchema], 500: dict})
    def list_bundles(self, request):
        """Get all bundles"""
        try:
            bundles = ProductBundle.objects.all()
            return 200, [BundleSchema.from_orm(bundle) for bundle in bundles]
        except Exception as e:
            logger.error(f"Error listing bundles: {e}")
            return 500, {
                "error": "An error occurred while fetching bundles",
                "message": str(e),
            }

    @http_get("/{id}", response={200: BundleSchema, 404: dict, 500: dict})
    def get_bundle(self, request, id: UUID):
        """Get a bundle by ID"""
        try:
            bundle = get_object_or_404(ProductBundle, id=id)
            return 200, bundle
        except Exception as e:
            logger.error(f"Error fetching bundle: {e}")
            return 500, {
                "error": "An error occurred while fetching bundle",
                "message": str(e),
            }

    @http_post("", response={201: BundleSchema})
    @transaction.atomic
    def create_bundle(self, data: BundleCreateSchema):
        """Create a new product bundle"""
        try:
            bundle = ProductBundle.objects.create(
                name=data.name,
                slug=data.slug,
                description=data.description,
                discount_percentage=data.discount_percentage,
                is_active=data.is_active,
                start_date=data.start_date,
                end_date=data.end_date,
            )

            for item in data.items:
                product = get_object_or_404(Product, id=item.product_id)
                BundleItem.objects.create(
                    bundle=bundle,
                    product=product,
                    quantity=item.quantity,
                    position=item.position,
                )

            return 201, bundle
        except Exception as e:
            logger.error(f"Error creating bundle: {e}")
            return 500, {
                "error": "An error occurred while creating bundle",
                "message": str(e),
            }

    @http_put("/{bundle_id}", response={200: BundleSchema})
    @transaction.atomic
    def update_bundle(self, bundle_id: UUID, data: BundleUpdateSchema):
        """Update a product bundle"""
        try:
            bundle = get_object_or_404(ProductBundle, id=bundle_id)

            for field, value in data.dict(
                exclude_unset=True, exclude={"items"}
            ).items():
                setattr(bundle, field, value)

            bundle.save()

            if data.items is not None:
                # Remove existing items
                bundle.items.all().delete()

                # Add new items
                for item in data.items:
                    product = get_object_or_404(Product, id=item.product_id)
                    BundleItem.objects.create(
                        bundle=bundle,
                        product=product,
                        quantity=item.quantity,
                        position=item.position,
                    )

            return 200, bundle
        except Exception as e:
            logger.error(f"Error updating bundle: {e}")
            return 500, {
                "error": "An error occurred while updating bundle",
                "message": str(e),
            }

    @http_delete("/{bundle_id}", response={204: None})
    def delete_bundle(self, bundle_id: UUID):
        """Delete a product bundle"""
        try:
            bundle = get_object_or_404(ProductBundle, id=bundle_id)
            bundle.delete()
            return 204, None
        except Exception as e:
            logger.error(f"Error deleting bundle: {e}")
            return 500, {
                "error": "An error occurred while deleting bundle",
                "message": str(e),
            }

    @http_get("/{bundle_id}/items", response={200: List[BundleItemSchema]})
    def list_bundle_items(self, bundle_id: UUID):
        """List all items in a bundle"""
        try:
            items = BundleItem.objects.filter(bundle_id=bundle_id)
            return 200, items
        except Exception as e:
            logger.error(f"Error fetching bundle items: {e}")
            return 500, {
                "error": "An error occurred while fetching bundle items",
                "message": str(e),
            }

    @http_post("/{bundle_id}/items", response={201: BundleItemSchema})
    def add_bundle_item(self, bundle_id: UUID, data: BundleItemCreateSchema):
        """Add an item to a bundle"""
        try:
            bundle = get_object_or_404(ProductBundle, id=bundle_id)
            product = get_object_or_404(Product, id=data.product_id)

            item = BundleItem.objects.create(
                bundle=bundle,
                product=product,
                quantity=data.quantity,
                position=data.position,
            )
            return 201, item
        except Exception as e:
            logger.error(f"Error adding bundle item: {e}")
            return 500, {
                "error": "An error occurred while adding bundle item",
                "message": str(e),
            }

    @http_put("/{bundle_id}/items/{item_id}", response={200: BundleItemSchema})
    def update_bundle_item(
        self, bundle_id: UUID, item_id: UUID, data: BundleItemUpdateSchema
    ):
        """Update a bundle item"""
        try:
            item = get_object_or_404(BundleItem, id=item_id, bundle_id=bundle_id)

            if data.product_id:
                item.product = get_object_or_404(Product, id=data.product_id)

            for field, value in data.dict(
                exclude_unset=True, exclude={"product_id"}
            ).items():
                setattr(item, field, value)

            item.save()
            return 200, item
        except Exception as e:
            logger.error(f"Error updating bundle item: {e}")
            return 500, {
                "error": "An error occurred while updating bundle item",
                "message": str(e),
            }

    @http_delete("/{bundle_id}/items/{item_id}", response={204: None})
    def delete_bundle_item(self, bundle_id: UUID, item_id: UUID):
        """Delete a bundle item"""
        try:
            item = get_object_or_404(BundleItem, id=item_id, bundle_id=bundle_id)
            item.delete()
            return 204, None
        except Exception as e:
            logger.error(f"Error deleting bundle item: {e}")
            return 500, {
                "error": "An error occurred while deleting bundle item",
                "message": str(e),
            }
