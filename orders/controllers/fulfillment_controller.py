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
from typing import List
from ninja_extra.permissions import IsAuthenticated
from ninja.pagination import paginate

from orders.models import (
    Order,
    OrderStatus,
    FulfillmentOrder,
    FulfillmentStatus,
    FulfillmentLineItem,
)
from orders.schemas import (
    FulfillmentSchema,
    FulfillmentCreateSchema,
)


@api_controller("/fulfillments", tags=["Order Fulfillments"])
class FulfillmentController:
    permission_classes = [IsAuthenticated]

    @http_get(
        "/",
        response={
            200: List[FulfillmentSchema],
            404: dict,
            500: dict,
        },
    )
    @paginate
    def list_fulfillments(self, request):
        """Get a paginated list of fulfillments."""
        try:
            fulfillments = (
                FulfillmentOrder.objects.select_related("order")
                .prefetch_related("items")
                .all()
            )
            return 200, fulfillments
        except Exception as e:
            return 500, {
                "error": "An error occurred while fetching fulfillments",
                "message": str(e),
            }

    @http_get(
        "/{fulfillment_id}",
        response={
            200: FulfillmentSchema,
            404: dict,
            500: dict,
        },
    )
    def get_fulfillment(self, request, fulfillment_id: str):
        """Get a single fulfillment by ID."""
        try:
            fulfillment = get_object_or_404(
                FulfillmentOrder.objects.select_related("order").prefetch_related(
                    "items"
                ),
                id=fulfillment_id,
            )
            return 200, fulfillment
        except FulfillmentOrder.DoesNotExist:
            return 404, {"error": "Fulfillment not found"}
        except Exception as e:
            return 500, {
                "error": "An error occurred while fetching the fulfillment",
                "message": str(e),
            }

    @http_post(
        "/",
        response={
            201: FulfillmentSchema,
            400: dict,
            404: dict,
            500: dict,
        },
    )
    @transaction.atomic
    def create_fulfillment(self, request, payload: FulfillmentCreateSchema):
        """Create a new fulfillment."""
        try:
            order = get_object_or_404(Order, id=payload.order_id)

            # Validate order state
            if order.status not in [OrderStatus.PENDING, OrderStatus.PARTIALLY_SHIPPED]:
                return 400, {"error": "Order cannot be fulfilled in its current status"}

            # Create fulfillment
            fulfillment = FulfillmentOrder.objects.create(
                order=order,
                status=FulfillmentStatus.PENDING,
                tracking_number=payload.tracking_number,
                tracking_url=payload.tracking_url,
                shipping_carrier=payload.shipping_carrier,
                shipping_method=payload.shipping_method,
                shipping_label_url=payload.shipping_label_url,
                notes=payload.notes,
                meta_data=payload.meta_data,
            )

            # Create fulfillment items
            for item in payload.items:
                order_item = order.items.get(id=item["order_item_id"])

                # Validate quantity
                if (
                    item["quantity"]
                    > order_item.quantity - order_item.fulfilled_quantity
                ):
                    return 400, {
                        "error": "Invalid fulfillment quantity",
                        "message": f"Requested quantity {item['quantity']} exceeds available quantity {order_item.quantity - order_item.fulfilled_quantity} for item {order_item.id}",
                    }

                FulfillmentLineItem.objects.create(
                    fulfillment=fulfillment,
                    order_item=order_item,
                    quantity=item["quantity"],
                )

                # Update order item fulfilled quantity
                order_item.fulfilled_quantity += item["quantity"]
                order_item.save()

            # Update order status if all items are fulfilled
            if all(
                item.quantity == item.fulfilled_quantity for item in order.items.all()
            ):
                order.status = OrderStatus.SHIPPED
            else:
                order.status = OrderStatus.PARTIALLY_SHIPPED
            order.save()

            return 201, fulfillment
        except Order.DoesNotExist:
            return 404, {"error": "Order not found"}
        except ValidationError as e:
            return 400, {"error": "Invalid data provided", "message": str(e)}
        except Exception as e:
            return 500, {
                "error": "An error occurred while creating the fulfillment",
                "message": str(e),
            }

    @http_put(
        "/{fulfillment_id}",
        response={
            200: FulfillmentSchema,
            400: dict,
            404: dict,
            500: dict,
        },
    )
    @transaction.atomic
    def update_fulfillment(
        self, request, fulfillment_id: str, payload: FulfillmentCreateSchema
    ):
        """Update an existing fulfillment."""
        try:
            fulfillment = get_object_or_404(FulfillmentOrder, id=fulfillment_id)

            # Only allow updates if fulfillment is in an editable state
            if fulfillment.status not in [
                FulfillmentStatus.PENDING,
                FulfillmentStatus.PROCESSING,
            ]:
                return 400, {
                    "error": "Fulfillment cannot be updated in its current status"
                }

            # Update fulfillment fields
            for field, value in payload.dict(exclude_unset=True).items():
                setattr(fulfillment, field, value)

            fulfillment.save()

            # If status is updated to SHIPPED, update order status
            if payload.status == FulfillmentStatus.SHIPPED:
                order = fulfillment.order
                if all(
                    f.status == FulfillmentStatus.SHIPPED
                    for f in order.fulfillments.all()
                ):
                    order.status = OrderStatus.SHIPPED
                    order.save()

            return 200, fulfillment
        except FulfillmentOrder.DoesNotExist:
            return 404, {"error": "Fulfillment not found"}
        except ValidationError as e:
            return 400, {"error": "Invalid data provided", "message": str(e)}
        except Exception as e:
            return 500, {
                "error": "An error occurred while updating the fulfillment",
                "message": str(e),
            }

    @http_delete(
        "/{fulfillment_id}",
        response={
            204: None,
            404: dict,
            500: dict,
        },
    )
    @transaction.atomic
    def delete_fulfillment(self, request, fulfillment_id: str):
        """Delete a fulfillment."""
        try:
            fulfillment = get_object_or_404(FulfillmentOrder, id=fulfillment_id)

            # Only allow deletion of pending fulfillments
            if fulfillment.status != FulfillmentStatus.PENDING:
                return 400, {"error": "Only pending fulfillments can be deleted"}

            # Restore order item fulfilled quantities
            for item in fulfillment.items.all():
                order_item = item.order_item
                order_item.fulfilled_quantity -= item.quantity
                order_item.save()

            # Update order status
            order = fulfillment.order
            if order.status in [OrderStatus.SHIPPED, OrderStatus.PARTIALLY_SHIPPED]:
                if any(item.fulfilled_quantity > 0 for item in order.items.all()):
                    order.status = OrderStatus.PARTIALLY_SHIPPED
                else:
                    order.status = OrderStatus.PENDING
                order.save()

            fulfillment.delete()
            return 204, None
        except FulfillmentOrder.DoesNotExist:
            return 404, {"error": "Fulfillment not found"}
        except Exception as e:
            return 500, {
                "error": "An error occurred while deleting the fulfillment",
                "message": str(e),
            }

    @http_post(
        "/{fulfillment_id}/ship",
        response={
            200: FulfillmentSchema,
            400: dict,
            404: dict,
            500: dict,
        },
    )
    @transaction.atomic
    def ship_fulfillment(self, request, fulfillment_id: str):
        """Mark a fulfillment as shipped."""
        try:
            fulfillment = get_object_or_404(FulfillmentOrder, id=fulfillment_id)

            # Validate fulfillment state
            if fulfillment.status != FulfillmentStatus.PENDING:
                return 400, {"error": "Only pending fulfillments can be shipped"}

            if not fulfillment.tracking_number:
                return 400, {"error": "Tracking number is required to ship fulfillment"}

            # Update fulfillment status
            fulfillment.status = FulfillmentStatus.SHIPPED
            fulfillment.save()

            # Update order status
            order = fulfillment.order
            if all(
                f.status == FulfillmentStatus.SHIPPED for f in order.fulfillments.all()
            ):
                order.status = OrderStatus.SHIPPED
                order.save()

            return 200, fulfillment
        except FulfillmentOrder.DoesNotExist:
            return 404, {"error": "Fulfillment not found"}
        except ValidationError as e:
            return 400, {"error": "Invalid fulfillment state", "message": str(e)}
        except Exception as e:
            return 500, {
                "error": "An error occurred while shipping the fulfillment",
                "message": str(e),
            }

    @http_post(
        "/{fulfillment_id}/cancel",
        response={
            200: FulfillmentSchema,
            400: dict,
            404: dict,
            500: dict,
        },
    )
    @transaction.atomic
    def cancel_fulfillment(self, request, fulfillment_id: str):
        """Cancel a fulfillment."""
        try:
            fulfillment = get_object_or_404(FulfillmentOrder, id=fulfillment_id)

            # Validate fulfillment state
            if fulfillment.status not in [
                FulfillmentStatus.PENDING,
                FulfillmentStatus.PROCESSING,
            ]:
                return 400, {
                    "error": "Fulfillment cannot be cancelled in its current status"
                }

            # Update fulfillment status
            fulfillment.status = FulfillmentStatus.CANCELLED
            fulfillment.save()

            # Restore order item fulfilled quantities
            for item in fulfillment.items.all():
                order_item = item.order_item
                order_item.fulfilled_quantity -= item.quantity
                order_item.save()

            # Update order status
            order = fulfillment.order
            if any(item.fulfilled_quantity > 0 for item in order.items.all()):
                order.status = OrderStatus.PARTIALLY_SHIPPED
            else:
                order.status = OrderStatus.PENDING
            order.save()

            return 200, fulfillment
        except FulfillmentOrder.DoesNotExist:
            return 404, {"error": "Fulfillment not found"}
        except ValidationError as e:
            return 400, {"error": "Invalid fulfillment state", "message": str(e)}
        except Exception as e:
            return 500, {
                "error": "An error occurred while cancelling the fulfillment",
                "message": str(e),
            }
