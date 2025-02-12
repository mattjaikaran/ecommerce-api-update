import logging
from typing import List
from decimal import Decimal
from django.db import transaction
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from ninja_extra import (
    api_controller,
    http_get,
    http_post,
    http_put,
    http_delete,
)
from ninja_extra.permissions import IsAuthenticated
from ninja.pagination import paginate

from orders.models import (
    Order,
    OrderLineItem,
    OrderStatus,
)
from orders.schemas import (
    OrderHistorySchema,
    OrderSchema,
    OrderCreateSchema,
    OrderUpdateSchema,
    OrderLineItemSchema,
    OrderLineItemCreateSchema,
    OrderLineItemUpdateSchema,
)

logger = logging.getLogger(__name__)


@api_controller("/orders", tags=["Orders"])
class OrderController:
    permission_classes = [IsAuthenticated]

    @http_get(
        "/",
        response={
            200: List[OrderSchema],
            404: dict,
            500: dict,
        },
    )
    @paginate
    def list_orders(self):
        """Get a paginated list of orders."""
        try:
            orders = (
                Order.objects.select_related(
                    "customer", "billing_address", "shipping_address"
                )
                .prefetch_related(
                    "items",
                    "fulfillments",
                    "transactions",
                    "refunds",
                    "taxes",
                    "notes",
                    "history",
                )
                .all()
            )
            return orders  # Return just the orders, not a tuple with status code
        except Exception as e:
            logger.error(f"Error fetching orders: {e}")
            return 500, {
                "error": "An error occurred while fetching orders",
                "message": str(e),
            }

    @http_get(
        "/{order_id}",
        response={
            200: OrderSchema,
            404: dict,
            500: dict,
        },
    )
    def get_order(self, request, order_id: str):
        """Get a single order by ID."""
        try:
            order = get_object_or_404(
                Order.objects.select_related(
                    "customer", "billing_address", "shipping_address"
                ).prefetch_related(
                    "items",
                    "fulfillments",
                    "transactions",
                    "refunds",
                    "taxes",
                    "notes",
                    "history",
                ),
                id=order_id,
            )
            return 200, order
        except Order.DoesNotExist:
            return 404, {"error": "Order not found"}
        except Exception as e:
            return 500, {
                "error": "An error occurred while fetching the order",
                "message": str(e),
            }

    @http_post(
        "/",
        response={
            201: OrderSchema,
            400: dict,
            404: dict,
            500: dict,
        },
    )
    @transaction.atomic
    def create_order(self, request, payload: OrderCreateSchema):
        """Create a new order."""
        try:
            # Create the order
            order = Order.objects.create(
                customer_id=payload.customer_id,
                customer_group_id=payload.customer_group_id,
                currency=payload.currency,
                shipping_method=payload.shipping_method,
                payment_method=payload.payment_method,
                payment_gateway=payload.payment_gateway,
                billing_address_id=payload.billing_address_id,
                shipping_address_id=payload.shipping_address_id,
                email=payload.email,
                phone=payload.phone,
                customer_note=payload.customer_note,
                meta_data=payload.meta_data,
                ip_address=request.META.get("REMOTE_ADDR"),
                user_agent=request.META.get("HTTP_USER_AGENT"),
            )

            # Create order items
            items = []
            subtotal = Decimal("0.00")
            for item in payload.items:
                order_item = OrderLineItem.objects.create(
                    order=order,
                    product_variant_id=item["product_variant_id"],
                    quantity=item["quantity"],
                )
                items.append(order_item)
                subtotal += order_item.total

            # Update order totals
            order.subtotal = subtotal
            order.total = (
                subtotal  # Will be updated by tax/shipping/discount calculations
            )
            order.save()

            return 201, order
        except ValidationError as e:
            return 400, {"error": "Invalid data provided", "message": str(e)}
        except Exception as e:
            return 500, {
                "error": "An error occurred while creating the order",
                "message": str(e),
            }

    @http_put(
        "/{order_id}",
        response={
            200: OrderSchema,
            400: dict,
            404: dict,
            500: dict,
        },
    )
    @transaction.atomic
    def update_order(self, request, order_id: str, payload: OrderUpdateSchema):
        """Update an existing order."""
        try:
            order = get_object_or_404(Order, id=order_id)

            # Only allow updates if order is in an editable state
            if order.status not in [OrderStatus.DRAFT, OrderStatus.PENDING]:
                return 400, {"error": "Order cannot be updated in its current status"}

            # Update order fields
            for field, value in payload.dict(exclude_unset=True).items():
                setattr(order, field, value)

            order.save()
            return 200, order
        except Order.DoesNotExist:
            return 404, {"error": "Order not found"}
        except ValidationError as e:
            return 400, {"error": "Invalid data provided", "message": str(e)}
        except Exception as e:
            return 500, {
                "error": "An error occurred while updating the order",
                "message": str(e),
            }

    @http_delete(
        "/{order_id}",
        response={
            204: None,
            404: dict,
            500: dict,
        },
    )
    @transaction.atomic
    def delete_order(self, request, order_id: str):
        """Delete an order (soft delete)."""
        try:
            order = get_object_or_404(Order, id=order_id)

            # Only allow deletion of draft orders
            if order.status != OrderStatus.DRAFT:
                return 400, {"error": "Only draft orders can be deleted"}

            order.is_deleted = True
            order.save()
            return 204, None
        except Order.DoesNotExist:
            return 404, {"error": "Order not found"}
        except Exception as e:
            return 500, {
                "error": "An error occurred while deleting the order",
                "message": str(e),
            }

    @http_post(
        "/{order_id}/items",
        response={
            201: OrderLineItemSchema,
            400: dict,
            404: dict,
            500: dict,
        },
    )
    @transaction.atomic
    def add_order_item(
        self, request, order_id: str, payload: OrderLineItemCreateSchema
    ):
        """Add an item to an order."""
        try:
            order = get_object_or_404(Order, id=order_id)

            # Only allow updates if order is in an editable state
            if order.status not in [OrderStatus.DRAFT, OrderStatus.PENDING]:
                return 400, {"error": "Order cannot be updated in its current status"}

            # Create order item
            order_item = OrderLineItem.objects.create(
                order=order,
                product_variant_id=payload.product_variant_id,
                quantity=payload.quantity,
            )

            # Update order totals
            order.subtotal += order_item.total
            order.total = (
                order.subtotal
            )  # Will be updated by tax/shipping/discount calculations
            order.save()

            return 201, order_item
        except Order.DoesNotExist:
            return 404, {"error": "Order not found"}
        except ValidationError as e:
            return 400, {"error": "Invalid data provided", "message": str(e)}
        except Exception as e:
            return 500, {
                "error": "An error occurred while adding the order item",
                "message": str(e),
            }

    @http_put(
        "/{order_id}/items/{item_id}",
        response={
            200: OrderLineItemSchema,
            400: dict,
            404: dict,
            500: dict,
        },
    )
    @transaction.atomic
    def update_order_item(
        self, request, order_id: str, item_id: str, payload: OrderLineItemUpdateSchema
    ):
        """Update an order item."""
        try:
            order = get_object_or_404(Order, id=order_id)
            order_item = get_object_or_404(OrderLineItem, id=item_id, order=order)

            # Only allow updates if order is in an editable state
            if order.status not in [OrderStatus.DRAFT, OrderStatus.PENDING]:
                return 400, {"error": "Order cannot be updated in its current status"}

            # Store old total for order total adjustment
            old_total = order_item.total

            # Update quantity
            order_item.quantity = payload.quantity
            order_item.save()

            # Update order totals
            order.subtotal = order.subtotal - old_total + order_item.total
            order.total = (
                order.subtotal
            )  # Will be updated by tax/shipping/discount calculations
            order.save()

            return 200, order_item
        except Order.DoesNotExist:
            return 404, {"error": "Order not found"}
        except OrderLineItem.DoesNotExist:
            return 404, {"error": "Order item not found"}
        except ValidationError as e:
            return 400, {"error": "Invalid data provided", "message": str(e)}
        except Exception as e:
            return 500, {
                "error": "An error occurred while updating the order item",
                "message": str(e),
            }

    @http_delete(
        "/{order_id}/items/{item_id}",
        response={
            204: None,
            404: dict,
            500: dict,
        },
    )
    @transaction.atomic
    def delete_order_item(self, request, order_id: str, item_id: str):
        """Delete an order item."""
        try:
            order = get_object_or_404(Order, id=order_id)
            order_item = get_object_or_404(OrderLineItem, id=item_id, order=order)

            # Only allow updates if order is in an editable state
            if order.status not in [OrderStatus.DRAFT, OrderStatus.PENDING]:
                return 400, {"error": "Order cannot be updated in its current status"}

            # Store total for order total adjustment
            item_total = order_item.total

            # Delete item
            order_item.delete()

            # Update order totals
            order.subtotal -= item_total
            order.total = (
                order.subtotal
            )  # Will be updated by tax/shipping/discount calculations
            order.save()

            return 204, None
        except Order.DoesNotExist:
            return 404, {"error": "Order not found"}
        except OrderLineItem.DoesNotExist:
            return 404, {"error": "Order item not found"}
        except Exception as e:
            return 500, {
                "error": "An error occurred while deleting the order item",
                "message": str(e),
            }

    @http_post(
        "/{order_id}/submit",
        response={
            200: OrderSchema,
            400: dict,
            404: dict,
            500: dict,
        },
    )
    @transaction.atomic
    def submit_order(self, request, order_id: str):
        """Submit a draft order for processing."""
        try:
            order = get_object_or_404(Order, id=order_id)

            # Validate order state
            if order.status != OrderStatus.DRAFT:
                return 400, {"error": "Only draft orders can be submitted"}

            if not order.items.exists():
                return 400, {"error": "Order must have at least one item"}

            # Update order status
            order.status = OrderStatus.PENDING
            order.save()

            # Additional business logic here (e.g. inventory checks, payment processing, etc.)

            return 200, order
        except Order.DoesNotExist:
            return 404, {"error": "Order not found"}
        except ValidationError as e:
            return 400, {"error": "Invalid order state", "message": str(e)}
        except Exception as e:
            return 500, {
                "error": "An error occurred while submitting the order",
                "message": str(e),
            }

    @http_post(
        "/{order_id}/cancel",
        response={
            200: OrderSchema,
            400: dict,
            404: dict,
            500: dict,
        },
    )
    @transaction.atomic
    def cancel_order(self, request, order_id: str):
        """Cancel an order."""
        try:
            order = get_object_or_404(Order, id=order_id)

            # Validate order state
            if order.status not in [OrderStatus.PENDING, OrderStatus.PARTIALLY_SHIPPED]:
                return 400, {"error": "Order cannot be cancelled in its current status"}

            # Update order status
            order.status = OrderStatus.CANCELLED
            order.save()

            # Additional business logic here (e.g. restore inventory, void payments, etc.)

            return 200, order
        except Order.DoesNotExist:
            return 404, {"error": "Order not found"}
        except ValidationError as e:
            return 400, {"error": "Invalid order state", "message": str(e)}
        except Exception as e:
            return 500, {
                "error": "An error occurred while cancelling the order",
                "message": str(e),
            }

    @http_get(
        "/{order_id}/history",
        response={
            200: List[OrderHistorySchema],
            404: dict,
            500: dict,
        },
    )
    def get_order_history(self, request, order_id: str):
        """Get the history of an order."""
        try:
            order = get_object_or_404(Order, id=order_id)
            return 200, order.history.all().order_by("-created_at")
        except Order.DoesNotExist:
            return 404, {"error": "Order not found"}
        except Exception as e:
            return 500, {
                "error": "An error occurred while fetching order history",
                "message": str(e),
            }
