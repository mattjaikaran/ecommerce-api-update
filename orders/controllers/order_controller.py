"""Order management controller with modern decorator-based approach."""

import logging
from decimal import Decimal

from django.db import transaction
from django.shortcuts import get_object_or_404
from ninja_extra import (
    api_controller,
    http_delete,
    http_get,
    http_post,
    http_put,
)

from api.decorators import (
    create_endpoint,
    delete_endpoint,
    detail_endpoint,
    list_endpoint,
    search_and_filter,
    update_endpoint,
)
from api.exceptions import ValidationError
from orders.models import (
    Order,
    OrderLineItem,
    OrderStatus,
)
from orders.schemas import (
    OrderCreateSchema,
    OrderHistorySchema,
    OrderLineItemCreateSchema,
    OrderLineItemSchema,
    OrderLineItemUpdateSchema,
    OrderSchema,
    OrderUpdateSchema,
)

logger = logging.getLogger(__name__)


@api_controller("/orders", tags=["Orders"])
class OrderController:
    """Order management controller with comprehensive decorators."""

    @http_get("", response={200: list[OrderSchema]})
    @list_endpoint(
        select_related=["customer", "billing_address", "shipping_address"],
        prefetch_related=["items__product_variant__product"],
        search_fields=["order_number", "email", "customer__user__username"],
        filter_fields={
            "status": "exact",
            "payment_status": "exact",
            "customer_id": "exact",
        },
        ordering_fields=["created_at", "order_number", "total", "status"],
    )
    @search_and_filter(
        search_fields=["order_number", "email", "customer__user__username"],
        filter_fields={
            "status": "exact",
            "payment_status": "exact",
        },
        ordering_fields=["created_at", "order_number", "total"],
    )
    def list_orders(self, request):
        """List all orders with advanced filtering and optimization."""
        return 200, Order.objects.all()

    @http_get("/{order_id}", response={200: OrderSchema, 404: dict})
    @detail_endpoint(
        select_related=[
            "customer__user",
            "billing_address",
            "shipping_address",
            "customer_group",
        ],
        prefetch_related=[
            "items__product_variant__product",
            "history",
            "notes",
        ],
    )
    def get_order(self, request, order_id: str):
        """Get a specific order by ID with optimized queries."""
        order = get_object_or_404(Order, id=order_id)
        return 200, order

    @http_post("", response={201: OrderSchema, 400: dict, 404: dict})
    @create_endpoint()
    @transaction.atomic
    def create_order(self, request, payload: OrderCreateSchema):
        """Create a new order."""
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
        subtotal = Decimal("0.00")
        for item in payload.items:
            order_item = OrderLineItem.objects.create(
                order=order,
                product_variant_id=item["product_variant_id"],
                quantity=item["quantity"],
            )
            subtotal += order_item.total

        # Update order totals
        order.subtotal = subtotal
        order.total = subtotal  # Will be updated by tax/shipping/discount calculations
        order.save()

        return 201, order

    @http_put("/{order_id}", response={200: OrderSchema, 400: dict, 404: dict})
    @update_endpoint()
    @transaction.atomic
    def update_order(self, request, order_id: str, payload: OrderUpdateSchema):
        """Update an order."""
        order = get_object_or_404(Order, id=order_id)

        # Only allow updates if order is in an editable state
        if order.status not in [OrderStatus.DRAFT, OrderStatus.PENDING]:
            validation_error = ValidationError(
                "Order cannot be updated in its current status"
            )
            raise validation_error

        # Update order fields
        for field, value in payload.dict(exclude_unset=True).items():
            setattr(order, field, value)

        order.save()
        return 200, order

    @http_delete("/{order_id}", response={204: None, 400: dict, 404: dict})
    @delete_endpoint()
    def delete_order(self, request, order_id: str):
        """Delete/Cancel an order."""
        order = get_object_or_404(Order, id=order_id)

        # Only allow deletion if order is in an editable state
        if order.status not in [OrderStatus.DRAFT, OrderStatus.PENDING]:
            validation_error = ValidationError(
                "Order cannot be deleted in its current status"
            )
            raise validation_error

        order.delete()
        return 204, None

    @http_post(
        "/{order_id}/items", response={201: OrderLineItemSchema, 400: dict, 404: dict}
    )
    @create_endpoint()
    @transaction.atomic
    def add_order_item(
        self, request, order_id: str, payload: OrderLineItemCreateSchema
    ):
        """Add an item to an order."""
        order = get_object_or_404(Order, id=order_id)

        # Only allow updates if order is in an editable state
        if order.status not in [OrderStatus.DRAFT, OrderStatus.PENDING]:
            validation_error = ValidationError(
                "Order cannot be updated in its current status"
            )
            raise validation_error

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

    @http_put(
        "/{order_id}/items/{item_id}",
        response={200: OrderLineItemSchema, 400: dict, 404: dict},
    )
    @update_endpoint()
    @transaction.atomic
    def update_order_item(
        self, request, order_id: str, item_id: str, payload: OrderLineItemUpdateSchema
    ):
        """Update an order item."""
        order = get_object_or_404(Order, id=order_id)
        order_item = get_object_or_404(OrderLineItem, id=item_id, order=order)

        # Only allow updates if order is in an editable state
        if order.status not in [OrderStatus.DRAFT, OrderStatus.PENDING]:
            validation_error = ValidationError(
                "Order cannot be updated in its current status"
            )
            raise validation_error

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

    @http_delete("/{order_id}/items/{item_id}", response={204: None, 404: dict})
    @delete_endpoint()
    @transaction.atomic
    def delete_order_item(self, request, order_id: str, item_id: str):
        """Delete an order item."""
        order = get_object_or_404(Order, id=order_id)
        order_item = get_object_or_404(OrderLineItem, id=item_id, order=order)

        # Only allow updates if order is in an editable state
        if order.status not in [OrderStatus.DRAFT, OrderStatus.PENDING]:
            validation_error = ValidationError(
                "Order cannot be updated in its current status"
            )
            raise validation_error

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

    @http_post("/{order_id}/submit", response={200: OrderSchema, 400: dict, 404: dict})
    @update_endpoint()
    @transaction.atomic
    def submit_order(self, request, order_id: str):
        """Submit a draft order for processing."""
        order = get_object_or_404(Order, id=order_id)

        # Validate order state
        if order.status != OrderStatus.DRAFT:
            validation_error = ValidationError("Only draft orders can be submitted")
            raise validation_error

        if not order.items.exists():
            validation_error = ValidationError("Order must have at least one item")
            raise validation_error

        # Update order status
        order.status = OrderStatus.PENDING
        order.save()

        # Additional business logic here (e.g. inventory checks, payment processing, etc.)

        return 200, order

    @http_post("/{order_id}/cancel", response={200: OrderSchema, 400: dict, 404: dict})
    @update_endpoint()
    @transaction.atomic
    def cancel_order(self, request, order_id: str):
        """Cancel an order."""
        order = get_object_or_404(Order, id=order_id)

        # Validate order state
        if order.status not in [OrderStatus.PENDING, OrderStatus.PARTIALLY_SHIPPED]:
            validation_error = ValidationError(
                "Order cannot be cancelled in its current status"
            )
            raise validation_error

        # Update order status
        order.status = OrderStatus.CANCELLED
        order.save()

        # Additional business logic here (e.g. restore inventory, void payments, etc.)

        return 200, order

    @http_get(
        "/{order_id}/history", response={200: list[OrderHistorySchema], 404: dict}
    )
    @list_endpoint(
        select_related=["order", "created_by"],
        ordering_fields=["created_at"],
    )
    def get_order_history(self, request, order_id: str):
        """Get the history of an order."""
        order = get_object_or_404(Order, id=order_id)
        return 200, order.history.all().order_by("-created_at")

    @http_get("/search", response={200: list[OrderSchema]})
    @list_endpoint(
        select_related=["customer", "billing_address", "shipping_address"],
        prefetch_related=["items__product_variant__product"],
        search_fields=["order_number", "email", "customer__user__username"],
        filter_fields={
            "status": "exact",
            "payment_status": "exact",
            "date_from": "date",
            "date_to": "date",
        },
        ordering_fields=["created_at", "order_number", "total"],
    )
    @search_and_filter(
        search_fields=["order_number", "email", "customer__user__username"],
        filter_fields={
            "status": "exact",
            "payment_status": "exact",
        },
        ordering_fields=["created_at", "order_number", "total"],
    )
    def search_orders(self, request):
        """Advanced order search with filtering."""
        return 200, Order.objects.all()
