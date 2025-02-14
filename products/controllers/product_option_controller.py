from typing import List
from uuid import UUID
from ninja_extra import api_controller, http_get, http_post, http_put, http_delete
from ninja_extra.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.core.exceptions import ValidationError
import logging

from products.models import ProductOption, ProductOptionValue
from products.schemas import (
    ProductOptionSchema,
    ProductOptionCreateSchema,
    ProductOptionUpdateSchema,
)

logger = logging.getLogger(__name__)


@api_controller("/products/options", tags=["Product Options"])
class ProductOptionController:
    permission_classes = [IsAuthenticated]

    @http_get("", response={200: List[ProductOptionSchema], 500: dict})
    def list_options(self):
        """
        Get all product options
        """
        try:
            options = ProductOption.objects.prefetch_related("values").all()
            return 200, options
        except Exception as e:
            logger.error(f"An error occurred while fetching options: {e}")
            return 500, {
                "error": "An error occurred while fetching options",
                "message": str(e),
            }

    @http_get("/{id}", response={200: ProductOptionSchema, 404: dict, 500: dict})
    def get_option(self, id: UUID):
        """
        Get a product option by ID
        """
        try:
            option = get_object_or_404(
                ProductOption.objects.prefetch_related("values"),
                id=id,
            )
            return 200, option
        except ProductOption.DoesNotExist:
            logger.error(f"Option not found with ID: {id}")
            return 404, {"error": "Option not found"}
        except Exception as e:
            logger.error(f"An error occurred while fetching the option: {e}")
            return 500, {
                "error": "An error occurred while fetching the option",
                "message": str(e),
            }

    @http_post("", response={201: ProductOptionSchema, 400: dict, 500: dict})
    @transaction.atomic
    def create_option(self, payload: ProductOptionCreateSchema):
        """
        Create a new product option with values
        """
        try:
            # Create option
            option = ProductOption.objects.create(
                name=payload.name,
                position=payload.position,
            )

            # Create option values
            for value_name in payload.values:
                ProductOptionValue.objects.create(
                    option=option,
                    name=value_name,
                )

            return 201, option
        except ValidationError as e:
            return 400, {"error": "Validation error", "message": str(e)}
        except Exception as e:
            return 500, {
                "error": "An error occurred while creating the option",
                "message": str(e),
            }

    @http_put(
        "/{id}", response={200: ProductOptionSchema, 400: dict, 404: dict, 500: dict}
    )
    @transaction.atomic
    def update_option(self, id: UUID, payload: ProductOptionUpdateSchema):
        """
        Update a product option and its values
        """
        try:
            option = get_object_or_404(ProductOption, id=id)

            # Update option fields
            option.name = payload.name
            option.position = payload.position
            option.save()

            # Update values if provided
            if payload.values:
                # Delete existing values
                option.values.all().delete()

                # Create new values
                for value_name in payload.values:
                    ProductOptionValue.objects.create(
                        option=option,
                        name=value_name,
                    )

            return 200, option
        except ProductOption.DoesNotExist:
            logger.error(f"Option not found with ID: {id}")
            return 404, {"error": "Option not found"}
        except ValidationError as e:
            logger.error(f"Validation error while updating option: {e}")
            return 400, {"error": "Validation error", "message": str(e)}
        except Exception as e:
            logger.error(f"An error occurred while updating the option: {e}")
            return 500, {
                "error": "An error occurred while updating the option",
                "message": str(e),
            }

    @http_delete("/{id}", response={204: dict, 400: dict, 404: dict, 500: dict})
    def delete_option(self, id: UUID):
        """
        Delete a product option
        """
        try:
            option = get_object_or_404(ProductOption, id=id)

            # Check if option is being used by any variants
            if option.productvariantoption_set.exists():
                logger.warning(
                    f"Cannot delete option {id} as it is being used by product variants"
                )
                return 400, {
                    "error": "Cannot delete option that is being used by product variants"
                }

            option.delete()
            return 204, {"message": "Option deleted successfully"}
        except ProductOption.DoesNotExist:
            logger.error(f"Option not found with ID: {id}")
            return 404, {"error": "Option not found"}
        except Exception as e:
            logger.error(f"An error occurred while deleting the option: {e}")
            return 500, {
                "error": "An error occurred while deleting the option",
                "message": str(e),
            }
