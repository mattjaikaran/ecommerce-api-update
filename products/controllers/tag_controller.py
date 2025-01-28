from typing import List
from ninja_extra import api_controller, http_get, http_post, http_put, http_delete
from ninja_extra.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.core.exceptions import ValidationError

from products.models import ProductTag, Product
from products.schemas.product import (
    ProductTagSchema,
    ProductTagCreateSchema,
    ProductTagUpdateSchema,
)


@api_controller("/tags", tags=["Product Tags"])
class TagController:
    permission_classes = [IsAuthenticated]

    @http_get("/", response={200: List[ProductTagSchema], 500: dict})
    def list_tags(self):
        """
        Get all product tags
        """
        try:
            tags = ProductTag.objects.prefetch_related("products").all()
            return 200, tags
        except Exception as e:
            return 500, {
                "error": "An error occurred while fetching tags",
                "message": str(e),
            }

    @http_get("/{id}", response={200: ProductTagSchema, 404: dict, 500: dict})
    def get_tag(self, id: str):
        """
        Get a product tag by ID
        """
        try:
            tag = get_object_or_404(
                ProductTag.objects.prefetch_related("products"),
                id=id,
            )
            return 200, tag
        except ProductTag.DoesNotExist:
            return 404, {"error": "Tag not found"}
        except Exception as e:
            return 500, {
                "error": "An error occurred while fetching the tag",
                "message": str(e),
            }

    @http_post("/", response={201: ProductTagSchema, 400: dict, 500: dict})
    @transaction.atomic
    def create_tag(self, payload: ProductTagCreateSchema):
        """
        Create a new product tag
        """
        try:
            tag = ProductTag.objects.create(**payload.dict())
            return 201, tag
        except ValidationError as e:
            return 400, {"error": "Validation error", "message": str(e)}
        except Exception as e:
            return 500, {
                "error": "An error occurred while creating the tag",
                "message": str(e),
            }

    @http_put(
        "/{id}", response={200: ProductTagSchema, 400: dict, 404: dict, 500: dict}
    )
    @transaction.atomic
    def update_tag(self, id: str, payload: ProductTagUpdateSchema):
        """
        Update a product tag
        """
        try:
            tag = get_object_or_404(ProductTag, id=id)
            for attr, value in payload.dict(exclude_unset=True).items():
                setattr(tag, attr, value)
            tag.save()
            return 200, tag
        except ProductTag.DoesNotExist:
            return 404, {"error": "Tag not found"}
        except ValidationError as e:
            return 400, {"error": "Validation error", "message": str(e)}
        except Exception as e:
            return 500, {
                "error": "An error occurred while updating the tag",
                "message": str(e),
            }

    @http_delete("/{id}", response={204: dict, 404: dict, 500: dict})
    def delete_tag(self, id: str):
        """
        Delete a product tag
        """
        try:
            tag = get_object_or_404(ProductTag, id=id)
            tag.delete()
            return 204, {"message": "Tag deleted successfully"}
        except ProductTag.DoesNotExist:
            return 404, {"error": "Tag not found"}
        except Exception as e:
            return 500, {
                "error": "An error occurred while deleting the tag",
                "message": str(e),
            }

    @http_post(
        "/{id}/products/{product_id}",
        response={200: ProductTagSchema, 404: dict, 500: dict},
    )
    def add_product(self, id: str, product_id: str):
        """
        Add a product to a tag
        """
        try:
            tag = get_object_or_404(ProductTag, id=id)
            product = get_object_or_404(Product, id=product_id)
            tag.products.add(product)
            return 200, tag
        except (ProductTag.DoesNotExist, Product.DoesNotExist):
            return 404, {"error": "Tag or product not found"}
        except Exception as e:
            return 500, {
                "error": "An error occurred while adding product to tag",
                "message": str(e),
            }

    @http_delete(
        "/{id}/products/{product_id}",
        response={200: ProductTagSchema, 404: dict, 500: dict},
    )
    def remove_product(self, id: str, product_id: str):
        """
        Remove a product from a tag
        """
        try:
            tag = get_object_or_404(ProductTag, id=id)
            product = get_object_or_404(Product, id=product_id)
            tag.products.remove(product)
            return 200, tag
        except (ProductTag.DoesNotExist, Product.DoesNotExist):
            return 404, {"error": "Tag or product not found"}
        except Exception as e:
            return 500, {
                "error": "An error occurred while removing product from tag",
                "message": str(e),
            }

    @http_post("/{id}/products", response={200: ProductTagSchema, 404: dict, 500: dict})
    def bulk_add_products(self, id: str, product_ids: List[str]):
        """
        Add multiple products to a tag
        """
        try:
            tag = get_object_or_404(ProductTag, id=id)
            products = Product.objects.filter(id__in=product_ids)
            tag.products.add(*products)
            return 200, tag
        except ProductTag.DoesNotExist:
            return 404, {"error": "Tag not found"}
        except Exception as e:
            return 500, {
                "error": "An error occurred while adding products to tag",
                "message": str(e),
            }

    @http_delete(
        "/{id}/products", response={200: ProductTagSchema, 404: dict, 500: dict}
    )
    def bulk_remove_products(self, id: str, product_ids: List[str]):
        """
        Remove multiple products from a tag
        """
        try:
            tag = get_object_or_404(ProductTag, id=id)
            products = Product.objects.filter(id__in=product_ids)
            tag.products.remove(*products)
            return 200, tag
        except ProductTag.DoesNotExist:
            return 404, {"error": "Tag not found"}
        except Exception as e:
            return 500, {
                "error": "An error occurred while removing products from tag",
                "message": str(e),
            }
