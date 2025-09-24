"""Payment management controller with modern decorator-based approach."""

import logging
from uuid import UUID

from django.shortcuts import get_object_or_404
from ninja_extra import api_controller, http_delete, http_get, http_post, http_put

from api.decorators import (
    create_endpoint,
    delete_endpoint,
    detail_endpoint,
    list_endpoint,
    search_and_filter,
    update_endpoint,
)
from payments.models import PaymentMethod, PaymentTransaction
from payments.schemas import (
    PaymentMethodCreateSchema,
    PaymentMethodSchema,
    PaymentMethodUpdateSchema,
    PaymentTransactionSchema,
)

logger = logging.getLogger(__name__)


@api_controller("/payments", tags=["Payments"])
class PaymentController:
    """Payment management controller with comprehensive decorators."""

    @http_get("/methods", response={200: list[PaymentMethodSchema]})
    @list_endpoint(
        select_related=["customer__user"],
        search_fields=["type", "provider", "customer__user__username"],
        filter_fields={
            "type": "exact",
            "provider": "exact",
            "is_active": "boolean",
            "customer_id": "exact",
        },
        ordering_fields=["created_at", "updated_at", "type", "provider"],
    )
    @search_and_filter(
        search_fields=["type", "provider", "customer__user__username"],
        filter_fields={
            "type": "exact",
            "provider": "exact",
            "is_active": "boolean",
        },
        ordering_fields=["created_at", "type", "provider"],
    )
    def get_payment_methods(self, request):
        """Get all payment methods with advanced filtering."""
        return 200, PaymentMethod.objects.filter(is_active=True)

    @http_get(
        "/methods/{payment_method_id}", response={200: PaymentMethodSchema, 404: dict}
    )
    @detail_endpoint(
        select_related=["customer__user"],
        prefetch_related=["transactions"],
    )
    def get_payment_method(self, request, payment_method_id: UUID):
        """Get a specific payment method by ID."""
        payment_method = get_object_or_404(
            PaymentMethod, id=payment_method_id, is_active=True
        )
        return 200, PaymentMethodSchema.from_orm(payment_method)

    @http_post("/methods", response={201: PaymentMethodSchema, 400: dict})
    @create_endpoint()
    def create_payment_method(self, request, payload: PaymentMethodCreateSchema):
        """Create a new payment method."""
        payment_method = PaymentMethod.objects.create(
            **payload.dict(),
            created_by=request.user,
            updated_by=request.user,
        )
        return 201, PaymentMethodSchema.from_orm(payment_method)

    @http_put(
        "/methods/{payment_method_id}",
        response={200: PaymentMethodSchema, 400: dict, 404: dict},
    )
    @update_endpoint()
    def update_payment_method(
        self, request, payment_method_id: UUID, payload: PaymentMethodUpdateSchema
    ):
        """Update a payment method."""
        payment_method = get_object_or_404(PaymentMethod, id=payment_method_id)

        for field, value in payload.dict(exclude_unset=True).items():
            setattr(payment_method, field, value)

        payment_method.updated_by = request.user
        payment_method.save()

        return 200, PaymentMethodSchema.from_orm(payment_method)

    @http_delete("/methods/{payment_method_id}", response={204: None, 404: dict})
    @delete_endpoint()
    def delete_payment_method(self, request, payment_method_id: UUID):
        """Soft delete a payment method."""
        payment_method = get_object_or_404(PaymentMethod, id=payment_method_id)
        payment_method.is_active = False
        payment_method.deleted_by = request.user
        payment_method.save()
        return 204, None

    @http_get("/transactions", response={200: list[PaymentTransactionSchema]})
    @list_endpoint(
        select_related=["payment_method__customer__user", "order"],
        search_fields=[
            "transaction_id",
            "gateway_transaction_id",
            "payment_method__customer__user__username",
        ],
        filter_fields={
            "status": "exact",
            "payment_method_id": "exact",
            "order_id": "exact",
            "gateway": "exact",
        },
        ordering_fields=["created_at", "amount", "status"],
    )
    @search_and_filter(
        search_fields=["transaction_id", "gateway_transaction_id"],
        filter_fields={
            "status": "exact",
            "gateway": "exact",
        },
        ordering_fields=["created_at", "amount", "status"],
    )
    def get_payment_transactions(self, request):
        """Get all payment transactions with advanced filtering."""
        return 200, PaymentTransaction.objects.all()

    @http_get(
        "/transactions/{transaction_id}",
        response={200: PaymentTransactionSchema, 404: dict},
    )
    @detail_endpoint(
        select_related=["payment_method__customer__user", "order"],
    )
    def get_payment_transaction(self, request, transaction_id: UUID):
        """Get a specific payment transaction by ID."""
        transaction = get_object_or_404(PaymentTransaction, id=transaction_id)
        return 200, PaymentTransactionSchema.from_orm(transaction)
