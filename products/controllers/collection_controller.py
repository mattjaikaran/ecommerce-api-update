import logging
from uuid import UUID

from django.db import transaction
from django.shortcuts import get_object_or_404
from ninja.pagination import paginate
from ninja_extra import api_controller, http_delete, http_get, http_post, http_put
from ninja_extra.permissions import IsAuthenticated

from api.decorators import handle_exceptions, log_api_call
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

    @http_get("", response={200: list[CollectionSchema]})
    @handle_exceptions
    @log_api_call()
    @paginate
    def list_collections(self, request):
        """Get paginated list of collections."""
        collections = ProductCollection.objects.prefetch_related("products").order_by(
            "name"
        )
        return 200, collections

    @http_get("/{id}", response={200: CollectionSchema})
    @handle_exceptions
    @log_api_call()
    def get_collection(self, request, id: UUID):
        """Get collection by ID."""
        collection = get_object_or_404(
            ProductCollection.objects.prefetch_related("products"), id=id
        )
        return 200, collection

    @http_post("", response={201: CollectionSchema})
    @handle_exceptions
    @log_api_call()
    @transaction.atomic
    def create_collection(self, request, payload: CollectionCreateSchema):
        """Create new collection."""
        collection = ProductCollection.objects.create(**payload.dict())
        return 201, collection

    @http_put("/{id}", response={200: CollectionSchema})
    @handle_exceptions
    @log_api_call()
    @transaction.atomic
    def update_collection(self, request, id: UUID, payload: CollectionUpdateSchema):
        """Update existing collection."""
        collection = get_object_or_404(ProductCollection, id=id)
        for attr, value in payload.dict(exclude_unset=True).items():
            setattr(collection, attr, value)
        collection.save()
        return 200, collection

    @http_delete("/{id}", response={204: None})
    @handle_exceptions
    @log_api_call()
    def delete_collection(self, request, id: UUID):
        """Delete collection."""
        collection = get_object_or_404(ProductCollection, id=id)
        collection.delete()
        return 204, None

    @http_post("/{id}/products/{product_id}", response={200: CollectionSchema})
    @handle_exceptions
    @log_api_call()
    def add_product(self, request, id: UUID, product_id: UUID):
        """Add product to collection."""
        collection = get_object_or_404(ProductCollection, id=id)
        product = get_object_or_404(Product, id=product_id)
        collection.products.add(product)
        return 200, collection

    @http_delete("/{id}/products/{product_id}", response={200: CollectionSchema})
    @handle_exceptions
    @log_api_call()
    def remove_product(self, request, id: UUID, product_id: UUID):
        """Remove product from collection."""
        collection = get_object_or_404(ProductCollection, id=id)
        product = get_object_or_404(Product, id=product_id)
        collection.products.remove(product)
        return 200, collection

    @http_post("/{id}/products/bulk", response={200: CollectionSchema})
    @handle_exceptions
    @log_api_call()
    def bulk_add_products(self, request, id: UUID, product_ids: list[UUID]):
        """Add multiple products to collection."""
        collection = get_object_or_404(ProductCollection, id=id)
        products = Product.objects.filter(id__in=product_ids)
        collection.products.add(*products)
        return 200, collection

    @http_delete("/{id}/products/bulk", response={200: CollectionSchema})
    @handle_exceptions
    @log_api_call()
    def bulk_remove_products(self, request, id: UUID, product_ids: list[UUID]):
        """Remove multiple products from collection."""
        collection = get_object_or_404(ProductCollection, id=id)
        products = Product.objects.filter(id__in=product_ids)
        collection.products.remove(*products)
        return 200, collection
