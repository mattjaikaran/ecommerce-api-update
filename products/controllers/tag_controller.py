import logging
from uuid import UUID

from django.db import transaction
from django.shortcuts import get_object_or_404
from ninja.pagination import paginate
from ninja_extra import api_controller, http_delete, http_get, http_post, http_put
from ninja_extra.permissions import IsAuthenticated

from api.decorators import handle_exceptions, log_api_call
from products.models import Product, ProductTag
from products.schemas import (
    ProductTagCreateSchema,
    ProductTagSchema,
    ProductTagUpdateSchema,
)

logger = logging.getLogger(__name__)


@api_controller("/products/tags", tags=["Product Tags"])
class TagController:
    permission_classes = [IsAuthenticated]

    @http_get("", response={200: list[ProductTagSchema]})
    @handle_exceptions
    @log_api_call()
    @paginate
    def list_tags(self, request):
        """Get paginated list of product tags."""
        tags = ProductTag.objects.prefetch_related("products").order_by("name")
        return 200, tags

    @http_get("/{id}", response={200: ProductTagSchema})
    @handle_exceptions
    @log_api_call()
    def get_tag(self, request, id: UUID):
        """Get product tag by ID."""
        tag = get_object_or_404(
            ProductTag.objects.prefetch_related("products"),
            id=id,
        )
        return 200, tag

    @http_post("", response={201: ProductTagSchema})
    @handle_exceptions
    @log_api_call()
    @transaction.atomic
    def create_tag(self, request, payload: ProductTagCreateSchema):
        """Create new product tag."""
        tag = ProductTag.objects.create(**payload.dict())
        return 201, tag

    @http_put("/{id}", response={200: ProductTagSchema})
    @handle_exceptions
    @log_api_call()
    @transaction.atomic
    def update_tag(self, request, id: UUID, payload: ProductTagUpdateSchema):
        """Update product tag."""
        tag = get_object_or_404(ProductTag, id=id)
        for attr, value in payload.dict(exclude_unset=True).items():
            setattr(tag, attr, value)
        tag.save()
        return 200, tag

    @http_delete("/{id}", response={204: None})
    @handle_exceptions
    @log_api_call()
    def delete_tag(self, request, id: UUID):
        """Delete product tag."""
        tag = get_object_or_404(ProductTag, id=id)
        tag.delete()
        return 204, None

    @http_post("/{id}/products/{product_id}", response={200: ProductTagSchema})
    @handle_exceptions
    @log_api_call()
    def add_product(self, request, id: UUID, product_id: UUID):
        """Add product to tag."""
        tag = get_object_or_404(ProductTag, id=id)
        product = get_object_or_404(Product, id=product_id)
        tag.products.add(product)
        return 200, tag

    @http_delete("/{id}/products/{product_id}", response={200: ProductTagSchema})
    @handle_exceptions
    @log_api_call()
    def remove_product(self, request, id: UUID, product_id: UUID):
        """Remove product from tag."""
        tag = get_object_or_404(ProductTag, id=id)
        product = get_object_or_404(Product, id=product_id)
        tag.products.remove(product)
        return 200, tag

    @http_post("/{id}/products/bulk", response={200: ProductTagSchema})
    @handle_exceptions
    @log_api_call()
    def bulk_add_products(self, request, id: UUID, product_ids: list[UUID]):
        """Add multiple products to tag."""
        tag = get_object_or_404(ProductTag, id=id)
        products = Product.objects.filter(id__in=product_ids)
        tag.products.add(*products)
        return 200, tag

    @http_delete("/{id}/products/bulk", response={200: ProductTagSchema})
    @handle_exceptions
    @log_api_call()
    def bulk_remove_products(self, request, id: UUID, product_ids: list[UUID]):
        """Remove multiple products from tag."""
        tag = get_object_or_404(ProductTag, id=id)
        products = Product.objects.filter(id__in=product_ids)
        tag.products.remove(*products)
        return 200, tag
