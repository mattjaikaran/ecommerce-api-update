from typing import List
from ninja_extra import api_controller, http_get, http_post, http_put, http_delete
from ninja_extra.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.core.exceptions import ValidationError
from uuid import UUID
import logging

from products.models import ProductReview, Product
from products.schemas import (
    ProductReviewSchema,
    ProductReviewCreateSchema,
    ProductReviewUpdateSchema,
)

logger = logging.getLogger(__name__)


@api_controller("/products/reviews", tags=["Product Reviews"])
class ReviewController:
    permission_classes = [IsAuthenticated]

    @http_get("", response={200: List[ProductReviewSchema], 500: dict})
    def list_reviews(self, request):
        """
        Get all product reviews
        """
        try:
            reviews = ProductReview.objects.select_related("product", "user").all()
            return 200, [ProductReviewSchema.from_orm(review) for review in reviews]
        except Exception as e:
            logger.error(f"Error listing reviews: {e}")
            return 500, {
                "error": "An error occurred while fetching reviews",
                "message": str(e),
            }

    @http_get("/{id}", response={200: ProductReviewSchema, 404: dict, 500: dict})
    def get_review(self, request, id: UUID):
        """
        Get a product review by ID
        """
        try:
            review = get_object_or_404(
                ProductReview.objects.select_related("product", "user"),
                id=id,
            )
            return 200, review
        except ProductReview.DoesNotExist:
            return 404, {"error": "Review not found"}
        except Exception as e:
            return 500, {
                "error": "An error occurred while fetching the review",
                "message": str(e),
            }

    @http_get(
        "/products/{product_id}",
        response={200: List[ProductReviewSchema], 404: dict, 500: dict},
    )
    def get_product_reviews(self, product_id: str):
        """
        Get all reviews for a specific product
        """
        try:
            reviews = ProductReview.objects.filter(
                product_id=product_id
            ).select_related("product", "user")
            return 200, reviews
        except Exception as e:
            return 500, {
                "error": "An error occurred while fetching product reviews",
                "message": str(e),
            }

    @http_post(
        "/", response={201: ProductReviewSchema, 400: dict, 404: dict, 500: dict}
    )
    @transaction.atomic
    def create_review(self, payload: ProductReviewCreateSchema, request):
        """
        Create a new product review
        """
        try:
            # Ensure product exists
            product = get_object_or_404(Product, id=payload.product_id)

            # Check if user has already reviewed this product
            if ProductReview.objects.filter(
                product=product, user=request.user
            ).exists():
                return 400, {"error": "User has already reviewed this product"}

            review = ProductReview.objects.create(
                product=product,
                user=request.user,
                rating=payload.rating,
                title=payload.title,
                comment=payload.comment,
            )
            return 201, review
        except Product.DoesNotExist:
            return 404, {"error": "Product not found"}
        except ValidationError as e:
            return 400, {"error": "Validation error", "message": str(e)}
        except Exception as e:
            return 500, {
                "error": "An error occurred while creating the review",
                "message": str(e),
            }

    @http_put(
        "/{id}", response={200: ProductReviewSchema, 400: dict, 404: dict, 500: dict}
    )
    @transaction.atomic
    def update_review(self, id: str, payload: ProductReviewUpdateSchema, request):
        """
        Update a product review
        """
        try:
            review = get_object_or_404(ProductReview, id=id)

            # Ensure user owns the review
            if review.user != request.user:
                return 403, {"error": "Not authorized to update this review"}

            review.rating = payload.rating
            review.title = payload.title
            review.comment = payload.comment
            review.save()

            return 200, review
        except ProductReview.DoesNotExist:
            return 404, {"error": "Review not found"}
        except ValidationError as e:
            return 400, {"error": "Validation error", "message": str(e)}
        except Exception as e:
            return 500, {
                "error": "An error occurred while updating the review",
                "message": str(e),
            }

    @http_delete("/{id}", response={204: dict, 404: dict, 500: dict})
    def delete_review(self, id: str, request):
        """
        Delete a product review
        """
        try:
            review = get_object_or_404(ProductReview, id=id)

            # Ensure user owns the review or is admin
            if review.user != request.user and not request.user.is_staff:
                return 403, {"error": "Not authorized to delete this review"}

            review.delete()
            return 204, {"message": "Review deleted successfully"}
        except ProductReview.DoesNotExist:
            return 404, {"error": "Review not found"}
        except Exception as e:
            return 500, {
                "error": "An error occurred while deleting the review",
                "message": str(e),
            }

    @http_put("/{id}/verify", response={200: ProductReviewSchema, 404: dict, 500: dict})
    def verify_review(self, id: str, request):
        """
        Verify a product review (admin only)
        """
        try:
            if not request.user.is_staff:
                return 403, {"error": "Only administrators can verify reviews"}

            review = get_object_or_404(ProductReview, id=id)
            review.is_verified = True
            review.save()

            return 200, review
        except ProductReview.DoesNotExist:
            return 404, {"error": "Review not found"}
        except Exception as e:
            return 500, {
                "error": "An error occurred while verifying the review",
                "message": str(e),
            }

    @http_put(
        "/{id}/feature", response={200: ProductReviewSchema, 404: dict, 500: dict}
    )
    def feature_review(self, id: str, request):
        """
        Feature/unfeature a product review (admin only)
        """
        try:
            if not request.user.is_staff:
                return 403, {"error": "Only administrators can feature reviews"}

            review = get_object_or_404(ProductReview, id=id)
            review.is_featured = not review.is_featured
            review.save()

            return 200, review
        except ProductReview.DoesNotExist:
            return 404, {"error": "Review not found"}
        except Exception as e:
            return 500, {
                "error": "An error occurred while featuring/unfeaturing the review",
                "message": str(e),
            }
