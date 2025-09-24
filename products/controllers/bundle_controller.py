import logging
from decimal import Decimal
from uuid import UUID

from django.db import transaction
from django.shortcuts import get_object_or_404
from ninja_extra import api_controller, http_delete, http_get, http_post, http_put
from ninja_extra.permissions import IsAuthenticated

from ..models import BundleItem, Product, ProductBundle
from ..schemas.bundle import (
    BundleCreateSchema,
    BundleItemCreateSchema,
    BundleItemSchema,
    BundleItemUpdateSchema,
    BundleSchema,
    BundleUpdateSchema,
)

logger = logging.getLogger(__name__)


@api_controller("/products/bundles", tags=["Product Bundles"])
class BundleController:
    permission_classes = [IsAuthenticated]

    @http_get("", response={200: list[BundleSchema], 500: dict})
    def list_bundles(self, request):
        """Get all bundles"""
        try:
            bundles = ProductBundle.objects.prefetch_related("items__product").all()
            bundle_list = []
            for bundle in bundles:
                # Calculate total price
                total_price = Decimal("0.00")
                for item in bundle.items.all():
                    total_price += item.product.price * item.quantity

                # Calculate discounted price
                discounted_price = total_price * (1 - bundle.discount_percentage / 100)

                # Create bundle dictionary with all fields
                bundle_dict = {
                    "id": bundle.id,
                    "name": bundle.name,
                    "slug": bundle.slug,
                    "description": bundle.description,
                    "discount_percentage": bundle.discount_percentage,
                    "total_price": total_price,
                    "discounted_price": discounted_price,
                    "is_active": bundle.is_active,
                    "start_date": bundle.start_date,
                    "end_date": bundle.end_date,
                    "meta_data": {},  # Add empty dict since it's required by schema
                    "items": [
                        BundleItemSchema.from_orm(item) for item in bundle.items.all()
                    ],
                    "created_at": bundle.created_at,
                    "updated_at": bundle.updated_at,
                    "date_modified": (
                        bundle.date_modified
                        if hasattr(bundle, "date_modified")
                        else None
                    ),
                }

                # Create BundleSchema from dictionary
                bundle_schema = BundleSchema.parse_obj(bundle_dict)
                bundle_list.append(bundle_schema)

            return 200, bundle_list
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

    @http_get("/{bundle_id}/items", response={200: list[BundleItemSchema]})
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
