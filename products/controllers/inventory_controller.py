import logging
from uuid import UUID

from django.db import transaction
from django.shortcuts import get_object_or_404
from ninja.pagination import paginate
from ninja_extra import api_controller, http_get, http_post
from ninja_extra.permissions import IsAuthenticated

from api.decorators import handle_exceptions, log_api_call
from api.exceptions import BadRequestError

from ..models import InventoryAction, Product, ProductInventoryHistory, ProductVariant
from ..schemas import (
    InventoryAdjustmentResponseSchema,
    InventoryAdjustmentSchema,
    InventoryHistorySchema,
)

logger = logging.getLogger(__name__)


@api_controller("/inventory", tags=["Inventory"], permissions=[IsAuthenticated])
class InventoryController:
    @http_get("/{product_id}/history", response={200: list[InventoryHistorySchema]})
    @handle_exceptions
    @log_api_call()
    @paginate
    def get_inventory_history(self, request, product_id: UUID):
        """Get inventory history for a product."""
        history = ProductInventoryHistory.objects.filter(
            product_id=product_id
        ).order_by("-created_at")
        return 200, history

    @http_get(
        "/{product_id}/variant/{variant_id}/history",
        response={200: list[InventoryHistorySchema]},
    )
    @handle_exceptions
    @log_api_call()
    @paginate
    def get_variant_inventory_history(
        self, request, product_id: UUID, variant_id: UUID
    ):
        """Get inventory history for a product variant."""
        history = ProductInventoryHistory.objects.filter(
            product_id=product_id, variant_id=variant_id
        ).order_by("-created_at")
        return 200, history

    @http_post(
        "/{product_id}/adjust", response={200: InventoryAdjustmentResponseSchema}
    )
    @handle_exceptions
    @log_api_call()
    @transaction.atomic
    def adjust_inventory(
        self, request, product_id: UUID, adjustment: InventoryAdjustmentSchema
    ):
        """Adjust inventory for a product or variant."""
        product = get_object_or_404(Product, id=product_id)

        if adjustment.variant_id:
            variant = get_object_or_404(ProductVariant, id=adjustment.variant_id)
            previous_quantity = variant.inventory_quantity
            variant.inventory_quantity = adjustment.new_quantity
            variant.save()

            history = ProductInventoryHistory.objects.create(
                product=product,
                variant=variant,
                action=InventoryAction.STOCK_ADJUST,
                quantity=adjustment.new_quantity - previous_quantity,
                previous_quantity=previous_quantity,
                new_quantity=adjustment.new_quantity,
                reference=adjustment.reference,
                notes=adjustment.notes,
            )
        else:
            previous_quantity = product.quantity
            product.quantity = adjustment.new_quantity
            product.save()

            history = ProductInventoryHistory.objects.create(
                product=product,
                action=InventoryAction.STOCK_ADJUST,
                quantity=adjustment.new_quantity - previous_quantity,
                previous_quantity=previous_quantity,
                new_quantity=adjustment.new_quantity,
                reference=adjustment.reference,
                notes=adjustment.notes,
            )

        return 200, {
            "success": True,
            "message": "Inventory adjusted successfully",
            "history": history,
        }

    @http_post("/{product_id}/add", response={200: InventoryAdjustmentResponseSchema})
    @handle_exceptions
    @log_api_call()
    @transaction.atomic
    def add_inventory(
        self, request, product_id: UUID, adjustment: InventoryAdjustmentSchema
    ):
        """Add inventory to a product or variant."""
        product = get_object_or_404(Product, id=product_id)

        if adjustment.variant_id:
            variant = get_object_or_404(ProductVariant, id=adjustment.variant_id)
            previous_quantity = variant.inventory_quantity
            variant.inventory_quantity += adjustment.quantity
            variant.save()

            history = ProductInventoryHistory.objects.create(
                product=product,
                variant=variant,
                action=InventoryAction.STOCK_ADD,
                quantity=adjustment.quantity,
                previous_quantity=previous_quantity,
                new_quantity=variant.inventory_quantity,
                reference=adjustment.reference,
                notes=adjustment.notes,
            )
        else:
            previous_quantity = product.quantity
            product.quantity += adjustment.quantity
            product.save()

            history = ProductInventoryHistory.objects.create(
                product=product,
                action=InventoryAction.STOCK_ADD,
                quantity=adjustment.quantity,
                previous_quantity=previous_quantity,
                new_quantity=product.quantity,
                reference=adjustment.reference,
                notes=adjustment.notes,
            )

        return 200, {
            "success": True,
            "message": "Inventory added successfully",
            "history": history,
        }

    @http_post(
        "/{product_id}/remove", response={200: InventoryAdjustmentResponseSchema}
    )
    @handle_exceptions
    @log_api_call()
    @transaction.atomic
    def remove_inventory(
        self, request, product_id: UUID, adjustment: InventoryAdjustmentSchema
    ):
        """Remove inventory from a product or variant."""
        product = get_object_or_404(Product, id=product_id)

        if adjustment.variant_id:
            variant = get_object_or_404(ProductVariant, id=adjustment.variant_id)
            if variant.inventory_quantity < adjustment.quantity:
                raise BadRequestError("Insufficient inventory")

            previous_quantity = variant.inventory_quantity
            variant.inventory_quantity -= adjustment.quantity
            variant.save()

            history = ProductInventoryHistory.objects.create(
                product=product,
                variant=variant,
                action=InventoryAction.STOCK_REMOVE,
                quantity=adjustment.quantity,
                previous_quantity=previous_quantity,
                new_quantity=variant.inventory_quantity,
                reference=adjustment.reference,
                notes=adjustment.notes,
            )
        else:
            if product.quantity < adjustment.quantity:
                raise BadRequestError("Insufficient inventory")

            previous_quantity = product.quantity
            product.quantity -= adjustment.quantity
            product.save()

            history = ProductInventoryHistory.objects.create(
                product=product,
                action=InventoryAction.STOCK_REMOVE,
                quantity=adjustment.quantity,
                previous_quantity=previous_quantity,
                new_quantity=product.quantity,
                reference=adjustment.reference,
                notes=adjustment.notes,
            )

        return 200, {
            "success": True,
            "message": "Inventory removed successfully",
            "history": history,
        }
