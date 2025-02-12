from typing import List
from ninja_extra import api_controller, http_get, http_post, http_put, http_delete
from ninja_extra.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.core.exceptions import ValidationError

from products.models import ProductCategory
from products.schemas import (
    CategorySchema,
    CategoryCreateSchema,
    CategoryUpdateSchema,
)


@api_controller("/categories", tags=["Product Categories"])
class CategoryController:
    permission_classes = [IsAuthenticated]

    @http_get(
        "/",
        response={
            200: List[CategorySchema],
            404: dict,
            500: dict,
        },
    )
    def list_categories(self):
        """
        Get all product categories
        """
        try:
            categories = ProductCategory.objects.prefetch_related(
                "children", "products"
            ).all()
            return 200, categories
        except ProductCategory.DoesNotExist:
            return 404, {"error": "Categories not found"}
        except Exception as e:
            return 500, {
                "error": "An error occurred while fetching categories",
                "message": str(e),
            }

    @http_get("/{id}", response=CategorySchema)
    def get_category(self, id: str):
        """
        Get a category by ID
        """
        try:
            category = get_object_or_404(
                ProductCategory.objects.prefetch_related("children", "products"),
                id=id,
            )
            return 200, category
        except ProductCategory.DoesNotExist:
            return 404, {"error": "Category not found"}
        except Exception as e:
            return 500, {
                "error": "An error occurred while fetching the category",
                "message": str(e),
            }

    @http_post(
        "/",
        response={
            201: CategorySchema,
            400: dict,
            404: dict,
            500: dict,
        },
    )
    @transaction.atomic
    def create_category(self, payload: CategoryCreateSchema):
        """
        Create a new category
        """
        try:
            # If parent_id is provided, verify it exists
            if payload.parent_id:
                get_object_or_404(ProductCategory, id=payload.parent_id)

            category = ProductCategory.objects.create(**payload.dict())
            return 201, category
        except ProductCategory.DoesNotExist:
            return 404, {"error": "Parent category not found"}
        except ValidationError as e:
            return 400, {"error": "Validation error", "message": str(e)}
        except Exception as e:
            return 500, {
                "error": "An error occurred while creating the category",
                "message": str(e),
            }

    @http_put(
        "/{id}",
        response={
            200: CategorySchema,
            400: dict,
            404: dict,
            500: dict,
        },
    )
    @transaction.atomic
    def update_category(self, id: str, payload: CategoryUpdateSchema):
        """
        Update a category
        """
        try:
            category = get_object_or_404(ProductCategory, id=id)

            # If parent_id is provided and changed, verify it exists and prevent circular reference
            if (
                payload.parent_id
                and payload.parent_id != category.parent_id
                and str(payload.parent_id) != str(id)
            ):
                get_object_or_404(ProductCategory, id=payload.parent_id)

                # Check for circular reference
                parent = ProductCategory.objects.get(id=payload.parent_id)
                while parent.parent_id:
                    if str(parent.parent_id) == str(id):
                        return 400, {
                            "error": "Circular reference detected in category hierarchy"
                        }
                    parent = parent.parent

            # Update fields
            for attr, value in payload.dict(exclude_unset=True).items():
                setattr(category, attr, value)
            category.save()

            return 200, category
        except ProductCategory.DoesNotExist:
            return 404, {"error": "Category not found"}
        except ValidationError as e:
            return 400, {"error": "Validation error", "message": str(e)}
        except Exception as e:
            return 500, {
                "error": "An error occurred while updating the category",
                "message": str(e),
            }

    @http_delete(
        "/{id}",
        response={
            204: dict,
            400: dict,
            404: dict,
            500: dict,
        },
    )
    def delete_category(self, id: str):
        """
        Delete a category
        """
        try:
            category = get_object_or_404(ProductCategory, id=id)

            # Check if category has children
            if category.children.exists():
                return 400, {
                    "error": "Cannot delete category with subcategories. Delete subcategories first."
                }

            # Check if category has products
            if category.products.exists():
                return 400, {
                    "error": "Cannot delete category with associated products. Remove or reassign products first."
                }

            category.delete()
            return 204, {"message": "Category deleted successfully"}
        except ProductCategory.DoesNotExist:
            return 404, {"error": "Category not found"}
        except Exception as e:
            return 500, {
                "error": "An error occurred while deleting the category",
                "message": str(e),
            }

    @http_get(
        "/tree",
        response={
            200: List[CategorySchema],
            500: dict,
        },
    )
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
            return 500, {
                "error": "An error occurred while fetching the category tree",
                "message": str(e),
            }
