import logging
from uuid import UUID

from django.db import transaction
from django.shortcuts import get_object_or_404
from ninja.pagination import paginate
from ninja_extra import api_controller, http_delete, http_get, http_post, http_put
from ninja_extra.permissions import IsAuthenticated

from api.decorators import handle_exceptions, log_api_call
from products.models import ProductCategory
from products.schemas import (
    CategoryCreateSchema,
    CategorySchema,
    CategoryUpdateSchema,
)

logger = logging.getLogger(__name__)


@api_controller("/products/categories", tags=["Product Categories"])
class CategoryController:
    permission_classes = [IsAuthenticated]

    @http_get("", response={200: list[CategorySchema]})
    @handle_exceptions
    @log_api_call()
    @paginate
    def list_categories(self, request):
        """Get paginated list of product categories."""
        categories = ProductCategory.objects.prefetch_related(
            "children", "products"
        ).order_by("name")
        return 200, categories

    @http_get("/{id}", response={200: CategorySchema})
    @handle_exceptions
    @log_api_call()
    def get_category(self, request, id: UUID):
        """Get category by ID."""
        category = get_object_or_404(
            ProductCategory.objects.prefetch_related("children", "products"),
            id=id,
        )
        return 200, category

    @http_post("", response={201: CategorySchema})
    @handle_exceptions
    @log_api_call()
    @transaction.atomic
    def create_category(self, request, payload: CategoryCreateSchema):
        """Create new product category."""
        category = ProductCategory.objects.create(**payload.dict())
        return 201, category

    @http_put("/{id}", response={200: CategorySchema})
    @handle_exceptions
    @log_api_call()
    @transaction.atomic
    def update_category(self, request, id: UUID, payload: CategoryUpdateSchema):
        """Update existing category."""
        category = get_object_or_404(ProductCategory, id=id)
        for attr, value in payload.dict(exclude_unset=True).items():
            setattr(category, attr, value)
        category.save()
        return 200, category

    @http_delete("/{id}", response={204: None})
    @handle_exceptions
    @log_api_call()
    def delete_category(self, request, id: UUID):
        """Delete category."""
        category = get_object_or_404(ProductCategory, id=id)
        category.delete()
        return 204, None

    @http_get("/tree", response={200: list[CategorySchema]})
    @handle_exceptions
    @log_api_call()
    def get_category_tree(self, request):
        """Get category tree (root categories with children)."""
        categories = ProductCategory.objects.filter(parent=None).prefetch_related(
            "children",
            "products",
        )
        return 200, categories
