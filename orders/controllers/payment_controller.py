from django.db import transaction
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from typing import List
from ninja_extra import (
    api_controller,
    route,
    http_get,
    http_post,
    http_put,
    http_delete,
)
from ninja_extra.permissions import IsAuthenticated
from ninja.pagination import paginate

from orders.models import (
    Order,
    OrderStatus,
    PaymentStatus,
    PaymentTransaction,
    Refund,
    RefundStatus,
)
from orders.schemas import (
    PaymentTransactionSchema,
    RefundSchema,
    RefundCreateSchema,
    RefundUpdateSchema,
)


@api_controller("/payments", tags=["Order Payments"])
class PaymentController:
    permission_classes = [IsAuthenticated]

    @http_get(
        "/",
        response={
            200: List[PaymentTransactionSchema],
            404: dict,
            500: dict,
        },
    )
    @paginate
    def list_payments(self, request):
        """Get a paginated list of payment transactions."""
        try:
            payments = PaymentTransaction.objects.select_related("order").all()
            return 200, payments
        except Exception as e:
            return 500, {
                "error": "An error occurred while fetching payments",
                "message": str(e),
            }

    @http_get(
        "/{payment_id}",
        response={
            200: PaymentTransactionSchema,
            404: dict,
            500: dict,
        },
    )
    def get_payment(self, request, payment_id: str):
        """Get a single payment transaction by ID."""
        try:
            payment = get_object_or_404(
                PaymentTransaction.objects.select_related("order"), id=payment_id
            )
            return 200, payment
        except PaymentTransaction.DoesNotExist:
            return 404, {"error": "Payment not found"}
        except Exception as e:
            return 500, {
                "error": "An error occurred while fetching the payment",
                "message": str(e),
            }

    @http_post(
        "/authorize",
        response={
            201: PaymentTransactionSchema,
            400: dict,
            404: dict,
            500: dict,
        },
    )
    @transaction.atomic
    def authorize_payment(
        self, request, order_id: str, amount: float, payment_method: str, gateway: str
    ):
        """Authorize a payment for an order."""
        try:
            order = get_object_or_404(Order, id=order_id)

            # Validate order state
            if order.status != OrderStatus.PENDING:
                return 400, {
                    "error": "Order cannot be authorized in its current status"
                }

            if order.payment_status != PaymentStatus.PENDING:
                return 400, {"error": "Payment has already been processed"}

            # Create payment transaction
            payment = PaymentTransaction.objects.create(
                order=order,
                transaction_id=f"AUTH_{order.order_number}",  # Replace with actual gateway transaction ID
                payment_method=payment_method,
                amount=amount,
                currency=order.currency,
                status=PaymentStatus.AUTHORIZED,
                gateway=gateway,
                gateway_response={},  # Replace with actual gateway response
            )

            # Update order payment status
            order.payment_status = PaymentStatus.AUTHORIZED
            order.payment_method = payment_method
            order.payment_gateway = gateway
            order.payment_gateway_id = payment.transaction_id
            order.save()

            return 201, payment
        except Order.DoesNotExist:
            return 404, {"error": "Order not found"}
        except ValidationError as e:
            return 400, {"error": "Invalid data provided", "message": str(e)}
        except Exception as e:
            return 500, {
                "error": "An error occurred while authorizing the payment",
                "message": str(e),
            }

    @http_post(
        "/capture/{payment_id}",
        response={
            200: PaymentTransactionSchema,
            400: dict,
            404: dict,
            500: dict,
        },
    )
    @transaction.atomic
    def capture_payment(self, request, payment_id: str, amount: float = None):
        """Capture an authorized payment."""
        try:
            payment = get_object_or_404(PaymentTransaction, id=payment_id)
            order = payment.order

            # Validate payment state
            if payment.status != PaymentStatus.AUTHORIZED:
                return 400, {"error": "Payment must be authorized before capture"}

            # Use authorized amount if no capture amount specified
            capture_amount = amount or payment.amount

            if capture_amount > payment.amount:
                return 400, {"error": "Capture amount cannot exceed authorized amount"}

            # Update payment transaction
            payment.status = PaymentStatus.PAID
            payment.amount = capture_amount
            payment.gateway_response = {}  # Replace with actual gateway response
            payment.save()

            # Update order payment status
            order.payment_status = PaymentStatus.PAID
            order.save()

            return 200, payment
        except PaymentTransaction.DoesNotExist:
            return 404, {"error": "Payment not found"}
        except ValidationError as e:
            return 400, {"error": "Invalid data provided", "message": str(e)}
        except Exception as e:
            return 500, {
                "error": "An error occurred while capturing the payment",
                "message": str(e),
            }

    @http_post(
        "/void/{payment_id}",
        response={
            200: PaymentTransactionSchema,
            400: dict,
            404: dict,
            500: dict,
        },
    )
    @transaction.atomic
    def void_payment(self, request, payment_id: str):
        """Void an authorized payment."""
        try:
            payment = get_object_or_404(PaymentTransaction, id=payment_id)
            order = payment.order

            # Validate payment state
            if payment.status != PaymentStatus.AUTHORIZED:
                return 400, {"error": "Only authorized payments can be voided"}

            # Update payment transaction
            payment.status = PaymentStatus.VOIDED
            payment.gateway_response = {}  # Replace with actual gateway response
            payment.save()

            # Update order payment status
            order.payment_status = PaymentStatus.VOIDED
            order.save()

            return 200, payment
        except PaymentTransaction.DoesNotExist:
            return 404, {"error": "Payment not found"}
        except ValidationError as e:
            return 400, {"error": "Invalid payment state", "message": str(e)}
        except Exception as e:
            return 500, {
                "error": "An error occurred while voiding the payment",
                "message": str(e),
            }

    @http_get(
        "/refunds",
        response={
            200: List[RefundSchema],
            404: dict,
            500: dict,
        },
    )
    @paginate
    def list_refunds(self, request):
        """Get a paginated list of refunds."""
        try:
            refunds = Refund.objects.select_related("order").all()
            return 200, refunds
        except Exception as e:
            return 500, {
                "error": "An error occurred while fetching refunds",
                "message": str(e),
            }

    @http_get(
        "/refunds/{refund_id}",
        response={
            200: RefundSchema,
            404: dict,
            500: dict,
        },
    )
    def get_refund(self, request, refund_id: str):
        """Get a single refund by ID."""
        try:
            refund = get_object_or_404(
                Refund.objects.select_related("order"), id=refund_id
            )
            return 200, refund
        except Refund.DoesNotExist:
            return 404, {"error": "Refund not found"}
        except Exception as e:
            return 500, {
                "error": "An error occurred while fetching the refund",
                "message": str(e),
            }

    @http_post(
        "/refunds",
        response={
            201: RefundSchema,
            400: dict,
            404: dict,
            500: dict,
        },
    )
    @transaction.atomic
    def create_refund(self, request, payload: RefundCreateSchema):
        """Create a new refund."""
        try:
            order = get_object_or_404(Order, id=payload.order_id)

            # Validate order state
            if order.status not in [OrderStatus.SHIPPED, OrderStatus.DELIVERED]:
                return 400, {"error": "Order cannot be refunded in its current status"}

            if order.payment_status != PaymentStatus.PAID:
                return 400, {"error": "Order must be paid before refund"}

            # Validate refund amount
            total_refunded = sum(r.amount for r in order.refunds.all())
            if total_refunded + payload.amount > order.total:
                return 400, {"error": "Refund amount exceeds order total"}

            # Create refund
            refund = Refund.objects.create(
                order=order,
                transaction_id=payload.transaction_id,
                amount=payload.amount,
                status=RefundStatus.PENDING,
                reason=payload.reason,
                notes=payload.notes,
                meta_data=payload.meta_data,
            )

            # Update order payment status
            if total_refunded + payload.amount == order.total:
                order.payment_status = PaymentStatus.REFUNDED
                order.status = OrderStatus.REFUNDED
            else:
                order.payment_status = PaymentStatus.PARTIALLY_REFUNDED
                order.status = OrderStatus.PARTIALLY_REFUNDED
            order.save()

            return 201, refund
        except Order.DoesNotExist:
            return 404, {"error": "Order not found"}
        except ValidationError as e:
            return 400, {"error": "Invalid data provided", "message": str(e)}
        except Exception as e:
            return 500, {
                "error": "An error occurred while creating the refund",
                "message": str(e),
            }

    @http_put(
        "/refunds/{refund_id}",
        response={
            200: RefundSchema,
            400: dict,
            404: dict,
            500: dict,
        },
    )
    @transaction.atomic
    def update_refund(self, request, refund_id: str, payload: RefundUpdateSchema):
        """Update an existing refund."""
        try:
            refund = get_object_or_404(Refund, id=refund_id)

            # Only allow updates if refund is in an editable state
            if refund.status not in [RefundStatus.PENDING, RefundStatus.PROCESSING]:
                return 400, {"error": "Refund cannot be updated in its current status"}

            # Update refund fields
            for field, value in payload.dict(exclude_unset=True).items():
                setattr(refund, field, value)

            refund.save()

            return 200, refund
        except Refund.DoesNotExist:
            return 404, {"error": "Refund not found"}
        except ValidationError as e:
            return 400, {"error": "Invalid data provided", "message": str(e)}
        except Exception as e:
            return 500, {
                "error": "An error occurred while updating the refund",
                "message": str(e),
            }

    @http_post(
        "/refunds/{refund_id}/process",
        response={
            200: RefundSchema,
            400: dict,
            404: dict,
            500: dict,
        },
    )
    @transaction.atomic
    def process_refund(self, request, refund_id: str):
        """Process a pending refund."""
        try:
            refund = get_object_or_404(Refund, id=refund_id)

            # Validate refund state
            if refund.status != RefundStatus.PENDING:
                return 400, {"error": "Only pending refunds can be processed"}

            # Process refund with payment gateway
            # Replace with actual gateway integration
            refund.status = RefundStatus.COMPLETED
            refund.refund_transaction_id = f"REF_{refund.order.order_number}"
            refund.gateway_response = {}  # Replace with actual gateway response
            refund.save()

            return 200, refund
        except Refund.DoesNotExist:
            return 404, {"error": "Refund not found"}
        except ValidationError as e:
            return 400, {"error": "Invalid refund state", "message": str(e)}
        except Exception as e:
            return 500, {
                "error": "An error occurred while processing the refund",
                "message": str(e),
            }
