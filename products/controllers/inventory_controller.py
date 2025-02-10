from typing import List
from uuid import UUID
from ninja_extra import api_controller, http_get, http_post
from ninja_extra.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import transaction
from ..models import Product, ProductVariant, ProductInventoryHistory, InventoryAction
from ..schemas import (
    InventoryHistorySchema,
    InventoryAdjustmentSchema,
    InventoryAdjustmentResponseSchema,
)
import logging

logger = logging.getLogger(__name__)


@api_controller("/inventory", tags=["Inventory"], permissions=[IsAuthenticated])
class InventoryController:
    @http_get("/{product_id}/history", response={200: List[InventoryHistorySchema]})
    def get_inventory_history(self, product_id: UUID):
        """Get inventory history for a product"""
        try:
            history = ProductInventoryHistory.objects.filter(product_id=product_id)
            return 200, history
        except Exception as e:
            logger.error(f"Error fetching inventory history: {e}")
            return 500, {
                "error": "An error occurred while fetching inventory history",
                "message": str(e),
            }

    @http_get(
        "/{product_id}/variant/{variant_id}/history",
        response={200: List[InventoryHistorySchema]},
    )
    def get_variant_inventory_history(self, product_id: UUID, variant_id: UUID):
        """Get inventory history for a product variant"""
        try:
            history = ProductInventoryHistory.objects.filter(
                product_id=product_id, variant_id=variant_id
            )
            return 200, history
        except Exception as e:
            logger.error(f"Error fetching variant inventory history: {e}")
            return 500, {
                "error": "An error occurred while fetching variant inventory history",
                "message": str(e),
            }

    @http_post(
        "/{product_id}/adjust", response={200: InventoryAdjustmentResponseSchema}
    )
    @transaction.atomic
    def adjust_inventory(self, product_id: UUID, adjustment: InventoryAdjustmentSchema):
        """Adjust inventory for a product or variant"""
        try:
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
        except Exception as e:
            logger.error(f"Error adjusting inventory: {e}")
            return 500, {
                "error": "An error occurred while adjusting inventory",
                "message": str(e),
            }

    @http_post("/{product_id}/add", response={200: InventoryAdjustmentResponseSchema})
    @transaction.atomic
    def add_inventory(self, product_id: UUID, adjustment: InventoryAdjustmentSchema):
        """Add inventory to a product or variant"""
        try:
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
        except Exception as e:
            logger.error(f"Error adding inventory: {e}")
            return 500, {
                "error": "An error occurred while adding inventory",
                "message": str(e),
            }

    @http_post(
        "/{product_id}/remove", response={200: InventoryAdjustmentResponseSchema}
    )
    @transaction.atomic
    def remove_inventory(self, product_id: UUID, adjustment: InventoryAdjustmentSchema):
        """Remove inventory from a product or variant"""
        try:
            product = get_object_or_404(Product, id=product_id)

            if adjustment.variant_id:
                variant = get_object_or_404(ProductVariant, id=adjustment.variant_id)
                if variant.inventory_quantity < adjustment.quantity:
                    return 400, {"error": "Insufficient inventory"}

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
                    return 400, {"error": "Insufficient inventory"}

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
        except Exception as e:
            logger.error(f"Error removing inventory: {e}")
            return 500, {
                "error": "An error occurred while removing inventory",
                "message": str(e),
            }
