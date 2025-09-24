import logging
from uuid import UUID

from django.core.exceptions import ValidationError
from django.db import transaction
from django.shortcuts import get_object_or_404
from ninja_extra import api_controller, http_delete, http_get, http_post, http_put
from ninja_extra.permissions import IsAuthenticated

from products.models import Product, ProductCollection
from products.schemas import (
    CollectionCreateSchema,
    CollectionSchema,
    CollectionUpdateSchema,
)

logger = logging.getLogger(__name__)


@api_controller("/products/collections", tags=["Collections"])
class CollectionController:
    permission_classes = [IsAuthenticated]

    @http_get(
        "", response={200: list[CollectionSchema], 400: dict, 404: dict, 500: dict}
    )
    def list_collections(self, request):
        """Get all collections"""
        try:
            collections = ProductCollection.objects.all()
            return 200, [
                CollectionSchema.from_orm(collection) for collection in collections
            ]
        except Exception as e:
            logger.error(f"Error listing collections: {e}")
            return 500, {
                "error": "An error occurred while fetching collections",
                "message": str(e),
            }

    @http_get("/{id}", response={200: CollectionSchema, 404: dict, 500: dict})
    def get_collection(self, request, id: UUID):
        """Get a collection by ID"""
        try:
            collection = get_object_or_404(ProductCollection, id=id)
            return 200, CollectionSchema.from_orm(collection)
        except ProductCollection.DoesNotExist:
            return 404, {"error": "Collection not found"}
        except Exception as e:
            logger.error(f"Error getting collection {id}: {e}")
            return 500, {
                "error": "An error occurred while fetching the collection",
                "message": str(e),
            }

    @http_post("", response={201: CollectionSchema, 400: dict, 500: dict})
    @transaction.atomic
    def create_collection(self, request, payload: CollectionCreateSchema):
        """Create a new collection"""
        try:
            collection = ProductCollection.objects.create(**payload.dict())
            return 201, CollectionSchema.from_orm(collection)
        except ValidationError as e:
            return 400, {"error": "Validation error", "message": str(e)}
        except Exception as e:
            logger.error(f"Error creating collection: {e}")
            return 500, {
                "error": "An error occurred while creating collection",
                "message": str(e),
            }

    @http_put(
        "/{id}", response={200: CollectionSchema, 400: dict, 404: dict, 500: dict}
    )
    @transaction.atomic
    def update_collection(self, request, id: UUID, payload: CollectionUpdateSchema):
        """Update a collection"""
        try:
            collection = get_object_or_404(ProductCollection, id=id)
            for attr, value in payload.dict(exclude_unset=True).items():
                setattr(collection, attr, value)
            collection.save()
            return 200, CollectionSchema.from_orm(collection)
        except ProductCollection.DoesNotExist:
            return 404, {"error": "Collection not found"}
        except ValidationError as e:
            return 400, {"error": "Validation error", "message": str(e)}
        except Exception as e:
            logger.error(f"Error updating collection {id}: {e}")
            return 500, {
                "error": "An error occurred while updating collection",
                "message": str(e),
            }

    @http_delete("/{id}", response={204: dict, 404: dict, 500: dict})
    def delete_collection(self, request, id: UUID):
        """Delete a collection"""
        try:
            collection = get_object_or_404(ProductCollection, id=id)
            collection.delete()
            return 204, {"message": "Collection deleted successfully"}
        except ProductCollection.DoesNotExist:
            return 404, {"error": "Collection not found"}
        except Exception as e:
            logger.error(f"Error deleting collection {id}: {e}")
            return 500, {
                "error": "An error occurred while deleting collection",
                "message": str(e),
            }

    @http_post(
        "/{id}/products/{product_id}",
        response={200: CollectionSchema, 404: dict, 500: dict},
    )
    def add_product(self, request, id: UUID, product_id: UUID):
        """Add a product to a collection"""
        try:
            collection = get_object_or_404(ProductCollection, id=id)
            product = get_object_or_404(Product, id=product_id)
            collection.products.add(product)
            return 200, CollectionSchema.from_orm(collection)
        except (ProductCollection.DoesNotExist, Product.DoesNotExist):
            return 404, {"error": "Collection or Product not found"}
        except Exception as e:
            logger.error(f"Error adding product {product_id} to collection {id}: {e}")
            return 500, {
                "error": "An error occurred while adding the product to the collection",
                "message": str(e),
            }

    @http_delete(
        "/{id}/products/{product_id}",
        response={200: CollectionSchema, 404: dict, 500: dict},
    )
    def remove_product(self, request, id: UUID, product_id: UUID):
        """Remove a product from a collection"""
        try:
            collection = get_object_or_404(ProductCollection, id=id)
            product = get_object_or_404(Product, id=product_id)
            collection.products.remove(product)
            return 200, CollectionSchema.from_orm(collection)
        except (ProductCollection.DoesNotExist, Product.DoesNotExist):
            return 404, {"error": "Collection or Product not found"}
        except Exception as e:
            logger.error(
                f"Error removing product {product_id} from collection {id}: {e}"
            )
            return 500, {
                "error": "An error occurred while removing the product from the collection",
                "message": str(e),
            }

    @http_post(
        "/{id}/products/bulk", response={200: CollectionSchema, 404: dict, 500: dict}
    )
    def bulk_add_products(self, request, id: UUID, product_ids: list[UUID]):
        """Add multiple products to a collection"""
        try:
            collection = get_object_or_404(ProductCollection, id=id)
            products = Product.objects.filter(id__in=product_ids)
            collection.products.add(*products)
            return 200, CollectionSchema.from_orm(collection)
        except ProductCollection.DoesNotExist:
            return 404, {"error": "Collection not found"}
        except Exception as e:
            logger.error(f"Error bulk adding products to collection {id}: {e}")
            return 500, {
                "error": "An error occurred while adding products to the collection",
                "message": str(e),
            }

    @http_delete(
        "/{id}/products/bulk", response={200: CollectionSchema, 404: dict, 500: dict}
    )
    def bulk_remove_products(self, request, id: UUID, product_ids: list[UUID]):
        """Remove multiple products from a collection"""
        try:
            collection = get_object_or_404(ProductCollection, id=id)
            products = Product.objects.filter(id__in=product_ids)
            collection.products.remove(*products)
            return 200, CollectionSchema.from_orm(collection)
        except ProductCollection.DoesNotExist:
            return 404, {"error": "Collection not found"}
        except Exception as e:
            logger.error(f"Error bulk removing products from collection {id}: {e}")
            return 500, {
                "error": "An error occurred while removing products from the collection",
                "message": str(e),
            }
