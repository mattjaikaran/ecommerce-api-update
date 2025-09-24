from django.db import transaction
from django.shortcuts import get_object_or_404
from ninja.pagination import paginate
from ninja_extra import (
    api_controller,
    http_get,
    http_post,
)
from ninja_extra.permissions import IsAuthenticated

from api.decorators import handle_exceptions, log_api_call
from api.exceptions import BadRequestError
from orders.models import (
    Order,
    OrderStatus,
    Tax,
    TaxType,
)
from orders.schemas import (
    TaxSchema,
)


@api_controller("/taxes", tags=["Order Taxes"])
class TaxController:
    permission_classes = [IsAuthenticated]

    @http_get("", response={200: list[TaxSchema]})
    @handle_exceptions
    @log_api_call()
    @paginate
    def list_taxes(self, request):
        """Get paginated list of taxes."""
        taxes = Tax.objects.select_related("order").order_by("-created_at")
        return 200, taxes

    @http_get("/{tax_id}", response={200: TaxSchema})
    @handle_exceptions
    @log_api_call()
    def get_tax(self, request, tax_id: str):
        """Get single tax by ID."""
        tax = get_object_or_404(Tax.objects.select_related("order"), id=tax_id)
        return 200, tax

    @http_get("/orders/{order_id}", response={200: list[TaxSchema]})
    @handle_exceptions
    @log_api_call()
    def get_order_taxes(self, request, order_id: str):
        """Get all taxes for a specific order."""
        order = get_object_or_404(Order, id=order_id)
        taxes = Tax.objects.filter(order=order).order_by("tax_type")
        return 200, taxes

    @http_post("/calculate/{order_id}", response={201: list[TaxSchema]})
    @handle_exceptions
    @log_api_call()
    @transaction.atomic
    def calculate_taxes(self, request, order_id: str):
        """Calculate and create taxes for an order."""
        order = get_object_or_404(Order, id=order_id)

        # Validate order state
        if order.status not in [OrderStatus.PENDING, OrderStatus.PROCESSING]:
            raise BadRequestError(
                "Taxes can only be calculated for pending or processing orders"
            )

        # Clear existing taxes
        Tax.objects.filter(order=order).delete()

        taxes = []

        # Calculate sales tax (simplified example)
        if order.shipping_address and order.shipping_address.state:
            sales_tax_rate = 0.08  # 8% example rate
            sales_tax_amount = order.subtotal * sales_tax_rate

            sales_tax = Tax.objects.create(
                order=order,
                tax_type=TaxType.SALES,
                rate=sales_tax_rate,
                amount=sales_tax_amount,
                name="Sales Tax",
                jurisdiction=order.shipping_address.state,
            )
            taxes.append(sales_tax)

        # Calculate VAT if applicable
        if hasattr(order, "requires_vat") and order.requires_vat:
            vat_rate = 0.20  # 20% example rate
            vat_amount = order.subtotal * vat_rate

            vat = Tax.objects.create(
                order=order,
                tax_type=TaxType.VAT,
                rate=vat_rate,
                amount=vat_amount,
                name="Value Added Tax",
                jurisdiction="EU",
            )
            taxes.append(vat)

        # Update order total
        total_tax = sum(tax.amount for tax in taxes)
        order.tax_total = total_tax
        order.total = order.subtotal + order.shipping_cost + total_tax
        order.save()

        return 201, taxes

    @http_post("/recalculate/{order_id}", response={200: list[TaxSchema]})
    @handle_exceptions
    @log_api_call()
    @transaction.atomic
    def recalculate_taxes(self, request, order_id: str):
        """Recalculate taxes for an existing order."""
        order = get_object_or_404(Order, id=order_id)

        # Validate order state
        if order.status == OrderStatus.CANCELLED:
            raise BadRequestError("Cannot recalculate taxes for cancelled orders")

        # Use the same logic as calculate_taxes
        return self.calculate_taxes(request, order_id)[1]  # Return the taxes list

    @http_get("/types", response={200: list[dict]})
    @handle_exceptions
    @log_api_call()
    def list_tax_types(self, request):
        """Get list of available tax types."""
        tax_types = [
            {"value": choice[0], "label": choice[1]} for choice in TaxType.choices
        ]
        return 200, tax_types
