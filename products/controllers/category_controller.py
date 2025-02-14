from typing import List
from ninja_extra import api_controller, http_get, http_post, http_put, http_delete
from ninja_extra.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.core.exceptions import ValidationError
from uuid import UUID

from products.models import ProductCategory
from products.schemas import (
    CategorySchema,
    CategoryCreateSchema,
    CategoryUpdateSchema,
)
import logging

logger = logging.getLogger(__name__)


@api_controller("/products/categories", tags=["Product Categories"])
class CategoryController:
    permission_classes = [IsAuthenticated]

    @http_get("", response={200: List[CategorySchema], 404: dict, 500: dict})
    def list_categories(self, request):
        """
        Get all product categories
        """
        try:
            categories = ProductCategory.objects.prefetch_related(
                "children", "products"
            ).all()
            return 200, [CategorySchema.from_orm(category) for category in categories]
        except ProductCategory.DoesNotExist:
            return 404, {"error": "Categories not found"}
        except Exception as e:
            logger.error(f"Error listing categories: {e}")
            return 500, {
                "error": "An error occurred while fetching categories",
                "message": str(e),
            }

    @http_get("/{id}", response={200: CategorySchema, 404: dict, 500: dict})
    def get_category(self, request, id: UUID):
        """
        Get a category by ID
        """
        try:
            category = get_object_or_404(
                ProductCategory.objects.prefetch_related("children", "products"),
                id=id,
            )
            return 200, CategorySchema.from_orm(category)
        except ProductCategory.DoesNotExist:
            return 404, {"error": "Category not found"}
        except Exception as e:
            logger.error(f"Error getting category {id}: {e}")
            return 500, {
                "error": "An error occurred while fetching category",
                "message": str(e),
            }

    @http_post("", response={201: CategorySchema, 400: dict, 500: dict})
    @transaction.atomic
    def create_category(self, request, payload: CategoryCreateSchema):
        """
        Create a new category
        """
        try:
            category = ProductCategory.objects.create(**payload.dict())
            return 201, CategorySchema.from_orm(category)
        except ValidationError as e:
            return 400, {"error": "Validation error", "message": str(e)}
        except Exception as e:
            logger.error(f"Error creating category: {e}")
            return 500, {
                "error": "An error occurred while creating category",
                "message": str(e),
            }

    @http_put("/{id}", response={200: CategorySchema, 400: dict, 404: dict, 500: dict})
    @transaction.atomic
    def update_category(self, request, id: UUID, payload: CategoryUpdateSchema):
        """
        Update a category
        """
        try:
            category = get_object_or_404(ProductCategory, id=id)
            for attr, value in payload.dict(exclude_unset=True).items():
                setattr(category, attr, value)
            category.save()
            return 200, CategorySchema.from_orm(category)
        except ProductCategory.DoesNotExist:
            return 404, {"error": "Category not found"}
        except ValidationError as e:
            return 400, {"error": "Validation error", "message": str(e)}
        except Exception as e:
            logger.error(f"Error updating category {id}: {e}")
            return 500, {
                "error": "An error occurred while updating category",
                "message": str(e),
            }

    @http_delete("/{id}", response={204: dict, 404: dict, 500: dict})
    def delete_category(self, request, id: UUID):
        """
        Delete a category
        """
        try:
            category = get_object_or_404(ProductCategory, id=id)
            category.delete()
            return 204, {"message": "Category deleted successfully"}
        except ProductCategory.DoesNotExist:
            return 404, {"error": "Category not found"}
        except Exception as e:
            logger.error(f"Error deleting category {id}: {e}")
            return 500, {
                "error": "An error occurred while deleting category",
                "message": str(e),
            }

    @http_get("/tree", response={200: List[CategorySchema], 500: dict})
    def get_category_tree(self):
        """
        Get category tree (only root categories with their children)
        """
        try:
            categories = ProductCategory.objects.filter(parent=None).prefetch_related(
                "children",
                "products",
            )
            return 200, categories
        except Exception as e:
            logger.error(f"Error fetching category tree: {e}")
            return 500, {
                "error": "An error occurred while fetching the category tree",
                "message": str(e),
            }
