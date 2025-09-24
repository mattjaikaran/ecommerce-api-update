import logging
from uuid import UUID

from django.db import transaction
from django.shortcuts import get_object_or_404
from ninja.pagination import paginate
from ninja_extra import api_controller, http_delete, http_get, http_post, http_put
from ninja_extra.permissions import IsAuthenticated

from api.decorators import handle_exceptions, log_api_call
from api.exceptions import BadRequestError
from products.models import ProductOption, ProductOptionValue
from products.schemas import (
    ProductOptionCreateSchema,
    ProductOptionSchema,
    ProductOptionUpdateSchema,
)

logger = logging.getLogger(__name__)


@api_controller("/products/options", tags=["Product Options"])
class ProductOptionController:
    permission_classes = [IsAuthenticated]

    @http_get("", response={200: list[ProductOptionSchema]})
    @handle_exceptions
    @log_api_call()
    @paginate
    def list_options(self, request):
        """Get paginated list of product options."""
        options = ProductOption.objects.prefetch_related("values").order_by(
            "position", "name"
        )
        return 200, options

    @http_get("/{id}", response={200: ProductOptionSchema})
    @handle_exceptions
    @log_api_call()
    def get_option(self, request, id: UUID):
        """Get product option by ID."""
        option = get_object_or_404(
            ProductOption.objects.prefetch_related("values"),
            id=id,
        )
        return 200, option

    @http_post("", response={201: ProductOptionSchema})
    @handle_exceptions
    @log_api_call()
    @transaction.atomic
    def create_option(self, request, payload: ProductOptionCreateSchema):
        """Create new product option with values."""
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

    @http_put("/{id}", response={200: ProductOptionSchema})
    @handle_exceptions
    @log_api_call()
    @transaction.atomic
    def update_option(self, request, id: UUID, payload: ProductOptionUpdateSchema):
        """Update product option and its values."""
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

    @http_delete("/{id}", response={204: None})
    @handle_exceptions
    @log_api_call()
    def delete_option(self, request, id: UUID):
        """Delete product option."""
        option = get_object_or_404(ProductOption, id=id)

        # Check if option is being used by any variants
        if option.productvariantoption_set.exists():
            raise BadRequestError(
                "Cannot delete option that is being used by product variants"
            )

        option.delete()
        return 204, None
