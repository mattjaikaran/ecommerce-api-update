from typing import List
from ninja_extra import api_controller, http_get, http_post, http_put, http_delete
from ninja_extra.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.core.exceptions import ValidationError

from products.models import ProductCollection, Product
from products.schemas import (
    ProductCollectionSchema,
    ProductCollectionCreateSchema,
    ProductCollectionUpdateSchema,
)


@api_controller("/collections", tags=["Product Collections"])
class CollectionController:
    permission_classes = [IsAuthenticated]

    @http_get("/", response={200: List[ProductCollectionSchema], 500: dict})
    def list_collections(self):
        """
        Get all product collections
        """
        try:
            collections = ProductCollection.objects.prefetch_related("products").all()
            return 200, collections
        except Exception as e:
            return 500, {
                "error": "An error occurred while fetching collections",
                "message": str(e),
            }

    @http_get("/{id}", response={200: ProductCollectionSchema, 404: dict, 500: dict})
    def get_collection(self, id: str):
        """
        Get a product collection by ID
        """
        try:
            collection = get_object_or_404(
                ProductCollection.objects.prefetch_related("products"),
                id=id,
            )
            return 200, collection
        except ProductCollection.DoesNotExist:
            return 404, {"error": "Collection not found"}
        except Exception as e:
            return 500, {
                "error": "An error occurred while fetching the collection",
                "message": str(e),
            }

    @http_post("/", response={201: ProductCollectionSchema, 400: dict, 500: dict})
    @transaction.atomic
    def create_collection(self, payload: ProductCollectionCreateSchema):
        """
        Create a new product collection
        """
        try:
            collection = ProductCollection.objects.create(**payload.dict())
            return 201, collection
        except ValidationError as e:
            return 400, {"error": "Validation error", "message": str(e)}
        except Exception as e:
            return 500, {
                "error": "An error occurred while creating the collection",
                "message": str(e),
            }

    @http_put(
        "/{id}",
        response={200: ProductCollectionSchema, 400: dict, 404: dict, 500: dict},
    )
    @transaction.atomic
    def update_collection(self, id: str, payload: ProductCollectionUpdateSchema):
        """
        Update a product collection
        """
        try:
            collection = get_object_or_404(ProductCollection, id=id)
            for attr, value in payload.dict(exclude_unset=True).items():
                setattr(collection, attr, value)
            collection.save()
            return 200, collection
        except ProductCollection.DoesNotExist:
            return 404, {"error": "Collection not found"}
        except ValidationError as e:
            return 400, {"error": "Validation error", "message": str(e)}
        except Exception as e:
            return 500, {
                "error": "An error occurred while updating the collection",
                "message": str(e),
            }

    @http_delete("/{id}", response={204: dict, 404: dict, 500: dict})
    def delete_collection(self, id: str):
        """
        Delete a product collection
        """
        try:
            collection = get_object_or_404(ProductCollection, id=id)
            collection.delete()
            return 204, {"message": "Collection deleted successfully"}
        except ProductCollection.DoesNotExist:
            return 404, {"error": "Collection not found"}
        except Exception as e:
            return 500, {
                "error": "An error occurred while deleting the collection",
                "message": str(e),
            }

    @http_post(
        "/{id}/products/{product_id}",
        response={200: ProductCollectionSchema, 404: dict, 500: dict},
    )
    def add_product(self, id: str, product_id: str):
        """
        Add a product to a collection
        """
        try:
            collection = get_object_or_404(ProductCollection, id=id)
            product = get_object_or_404(Product, id=product_id)
            collection.products.add(product)
            return 200, collection
        except (ProductCollection.DoesNotExist, Product.DoesNotExist):
            return 404, {"error": "Collection or product not found"}
        except Exception as e:
            return 500, {
                "error": "An error occurred while adding product to collection",
                "message": str(e),
            }

    @http_delete(
        "/{id}/products/{product_id}",
        response={200: ProductCollectionSchema, 404: dict, 500: dict},
    )
    def remove_product(self, id: str, product_id: str):
        """
        Remove a product from a collection
        """
        try:
            collection = get_object_or_404(ProductCollection, id=id)
            product = get_object_or_404(Product, id=product_id)
            collection.products.remove(product)
            return 200, collection
        except (ProductCollection.DoesNotExist, Product.DoesNotExist):
            return 404, {"error": "Collection or product not found"}
        except Exception as e:
            return 500, {
                "error": "An error occurred while removing product from collection",
                "message": str(e),
            }

    @http_post(
        "/{id}/products", response={200: ProductCollectionSchema, 404: dict, 500: dict}
    )
    def bulk_add_products(self, id: str, product_ids: List[str]):
        """
        Add multiple products to a collection
        """
        try:
            collection = get_object_or_404(ProductCollection, id=id)
            products = Product.objects.filter(id__in=product_ids)
            collection.products.add(*products)
            return 200, collection
        except ProductCollection.DoesNotExist:
            return 404, {"error": "Collection not found"}
        except Exception as e:
            return 500, {
                "error": "An error occurred while adding products to collection",
                "message": str(e),
            }

    @http_delete(
        "/{id}/products", response={200: ProductCollectionSchema, 404: dict, 500: dict}
    )
    def bulk_remove_products(self, id: str, product_ids: List[str]):
        """
        Remove multiple products from a collection
        """
        try:
            collection = get_object_or_404(ProductCollection, id=id)
            products = Product.objects.filter(id__in=product_ids)
            collection.products.remove(*products)
            return 200, collection
        except ProductCollection.DoesNotExist:
            return 404, {"error": "Collection not found"}
        except Exception as e:
            return 500, {
                "error": "An error occurred while removing products from collection",
                "message": str(e),
            }
