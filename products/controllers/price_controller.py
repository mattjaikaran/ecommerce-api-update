from typing import List
from uuid import UUID
from ninja_extra import api_controller, http_get, http_post, http_put
from ninja_extra.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import transaction
from ..models import Product, ProductVariant, ProductPriceHistory, PriceAction
from ..schemas.price import (
    PriceHistorySchema,
    PriceAdjustmentSchema,
    PriceAdjustmentResponseSchema,
)
import logging

logger = logging.getLogger(__name__)


@api_controller("/prices", tags=["Prices"], permissions=[IsAuthenticated])
class PriceController:
    @http_get("/{product_id}/history", response={200: List[PriceHistorySchema]})
    def get_price_history(self, product_id: UUID):
        """Get price history for a product"""
        try:
            history = ProductPriceHistory.objects.filter(product_id=product_id)
            return 200, history
        except Exception as e:
            logger.error(f"Error fetching price history: {e}")
            return 500, {
                "error": "An error occurred while fetching price history",
                "message": str(e),
            }

    @http_get(
        "/{product_id}/variant/{variant_id}/history",
        response={200: List[PriceHistorySchema]},
    )
    def get_variant_price_history(self, product_id: UUID, variant_id: UUID):
        """Get price history for a product variant"""
        try:
            history = ProductPriceHistory.objects.filter(
                product_id=product_id, variant_id=variant_id
            )
            return 200, history
        except Exception as e:
            logger.error(f"Error fetching variant price history: {e}")
            return 500, {
                "error": "An error occurred while fetching variant price history",
                "message": str(e),
            }

    @http_post("/{product_id}/adjust", response={200: PriceAdjustmentResponseSchema})
    @transaction.atomic
    def adjust_price(self, product_id: UUID, adjustment: PriceAdjustmentSchema):
        """Adjust price for a product or variant"""
        try:
            product = get_object_or_404(Product, id=product_id)

            if adjustment.variant_id:
                variant = get_object_or_404(ProductVariant, id=adjustment.variant_id)
                previous_price = variant.price
                variant.price = adjustment.new_price

                if adjustment.action == PriceAction.SALE_PRICE:
                    variant.compare_at_price = previous_price
                elif adjustment.action == PriceAction.COST_PRICE:
                    variant.cost_price = adjustment.new_price

                variant.save()

                history = ProductPriceHistory.objects.create(
                    product=product,
                    variant=variant,
                    action=adjustment.action,
                    previous_price=previous_price,
                    new_price=adjustment.new_price,
                    reason=adjustment.reason,
                    notes=adjustment.notes,
                )
            else:
                previous_price = product.price
                product.price = adjustment.new_price

                if adjustment.action == PriceAction.SALE_PRICE:
                    product.compare_at_price = previous_price
                elif adjustment.action == PriceAction.COST_PRICE:
                    product.cost_price = adjustment.new_price

                product.save()

                history = ProductPriceHistory.objects.create(
                    product=product,
                    action=adjustment.action,
                    previous_price=previous_price,
                    new_price=adjustment.new_price,
                    reason=adjustment.reason,
                    notes=adjustment.notes,
                )

            return 200, {
                "success": True,
                "message": "Price adjusted successfully",
                "history": history,
            }
        except Exception as e:
            logger.error(f"Error adjusting price: {e}")
            return 500, {
                "error": "An error occurred while adjusting price",
                "message": str(e),
            }

    @http_post(
        "/{product_id}/bulk-adjust", response={200: List[PriceAdjustmentResponseSchema]}
    )
    @transaction.atomic
    def bulk_adjust_prices(
        self, product_id: UUID, adjustments: List[PriceAdjustmentSchema]
    ):
        """Bulk adjust prices for product variants"""
        try:
            product = get_object_or_404(Product, id=product_id)
            results = []

            for adjustment in adjustments:
                if adjustment.variant_id:
                    variant = get_object_or_404(
                        ProductVariant, id=adjustment.variant_id
                    )
                    previous_price = variant.price
                    variant.price = adjustment.new_price

                    if adjustment.action == PriceAction.SALE_PRICE:
                        variant.compare_at_price = previous_price
                    elif adjustment.action == PriceAction.COST_PRICE:
                        variant.cost_price = adjustment.new_price

                    variant.save()

                    history = ProductPriceHistory.objects.create(
                        product=product,
                        variant=variant,
                        action=adjustment.action,
                        previous_price=previous_price,
                        new_price=adjustment.new_price,
                        reason=adjustment.reason,
                        notes=adjustment.notes,
                    )

                    results.append(
                        {
                            "success": True,
                            "message": f"Price adjusted successfully for variant {variant.id}",
                            "history": history,
                        }
                    )

            return 200, results
        except Exception as e:
            logger.error(f"Error bulk adjusting prices: {e}")
            return 500, {
                "error": "An error occurred while bulk adjusting prices",
                "message": str(e),
            }
