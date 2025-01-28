from django.db import transaction
from typing import List
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

    @http_get(
        "/",
        response={
            200: List[TaxSchema],
            404: dict,
            500: dict,
        },
    )
    @paginate
    def list_taxes(self, request):
        """Get a paginated list of taxes."""
        try:
            taxes = Tax.objects.select_related("order").all()
            return 200, taxes
        except Exception as e:
            return 500, {
                "error": "An error occurred while fetching taxes",
                "message": str(e),
            }

    @http_get(
        "/{tax_id}",
        response={
            200: TaxSchema,
            404: dict,
            500: dict,
        },
    )
    def get_tax(self, request, tax_id: str):
        """Get a single tax by ID."""
        try:
            tax = get_object_or_404(Tax.objects.select_related("order"), id=tax_id)
            return 200, tax
        except Tax.DoesNotExist:
            return 404, {"error": "Tax not found"}
        except Exception as e:
            return 500, {
                "error": "An error occurred while fetching the tax",
                "message": str(e),
            }

    @http_post(
        "/calculate/{order_id}",
        response={
            200: dict,
            400: dict,
            404: dict,
            500: dict,
        },
    )
    @transaction.atomic
    def calculate_taxes(self, request, order_id: str):
        """Calculate taxes for an order."""
        try:
            order = get_object_or_404(Order, id=order_id)

            # Only calculate taxes for draft or pending orders
            if order.status not in [OrderStatus.DRAFT, OrderStatus.PENDING]:
                return 400, {
                    "error": "Taxes cannot be calculated for this order status"
                }

            # Clear existing taxes
            order.taxes.all().delete()

            # Initialize tax totals
            tax_amount = 0
            shipping_tax_amount = 0

            # Calculate item taxes
            for item in order.items.all():
                # Example tax calculation - replace with actual tax service integration
                if item.product_variant.taxable:
                    tax_rate = 0.1  # 10% tax rate - replace with actual tax rate lookup
                    item_tax = item.total * tax_rate

                    Tax.objects.create(
                        order=order,
                        tax_type=TaxType.SALES_TAX,
                        name="Sales Tax",
                        rate=tax_rate,
                        amount=item_tax,
                        jurisdiction="Example State",  # Replace with actual jurisdiction
                        meta_data={
                            "item_id": str(item.id),
                            "product_id": str(item.product_variant.product_id),
                        },
                    )
                    tax_amount += item_tax

            # Calculate shipping tax if applicable
            if order.shipping_amount > 0:
                shipping_tax_rate = (
                    0.1  # 10% tax rate - replace with actual tax rate lookup
                )
                shipping_tax = order.shipping_amount * shipping_tax_rate

                Tax.objects.create(
                    order=order,
                    tax_type=TaxType.SHIPPING_TAX,
                    name="Shipping Tax",
                    rate=shipping_tax_rate,
                    amount=shipping_tax,
                    jurisdiction="Example State",  # Replace with actual jurisdiction
                    meta_data={"shipping_method": order.shipping_method},
                )
                shipping_tax_amount += shipping_tax

            # Update order tax amounts
            order.tax_amount = tax_amount
            order.shipping_tax_amount = shipping_tax_amount
            order.total = (
                order.subtotal
                + order.shipping_amount
                + tax_amount
                + shipping_tax_amount
                - order.discount_amount
            )
            order.save()

            return 200, {
                "tax_amount": tax_amount,
                "shipping_tax_amount": shipping_tax_amount,
                "total_tax": tax_amount + shipping_tax_amount,
                "taxes": order.taxes.all(),
            }
        except Order.DoesNotExist:
            return 404, {"error": "Order not found"}
        except ValidationError as e:
            return 400, {"error": "Invalid data provided", "message": str(e)}
        except Exception as e:
            return 500, {
                "error": "An error occurred while calculating taxes",
                "message": str(e),
            }

    @http_get(
        "/rates",
        response={
            200: dict,
            404: dict,
            500: dict,
        },
    )
    def get_tax_rates(self, request, postal_code: str, country: str):
        """Get tax rates for a location."""
        try:
            # Example tax rate lookup - replace with actual tax service integration
            rates = {
                "sales_tax": 0.1,  # 10%
                "shipping_tax": 0.1,  # 10%
                "digital_tax": 0.1,  # 10%
                "jurisdiction": "Example State",
                "postal_code": postal_code,
                "country": country,
            }
            return 200, rates
        except Exception as e:
            return 500, {
                "error": "An error occurred while fetching tax rates",
                "message": str(e),
            }

    @http_get(
        "/jurisdictions",
        response={
            200: dict,
            404: dict,
            500: dict,
        },
    )
    def get_tax_jurisdictions(self, request, postal_code: str, country: str):
        """Get tax jurisdictions for a location."""
        try:
            # Example jurisdiction lookup - replace with actual tax service integration
            jurisdictions = {
                "country": {
                    "code": country,
                    "name": "Example Country",
                    "rate": 0.05,  # 5%
                },
                "state": {"code": "EX", "name": "Example State", "rate": 0.04},  # 4%
                "county": {"code": "EXC", "name": "Example County", "rate": 0.01},  # 1%
                "city": {"code": "EXCITY", "name": "Example City", "rate": 0.0},  # 0%
                "postal_code": postal_code,
                "combined_rate": 0.1,  # 10%
            }
            return 200, jurisdictions
        except Exception as e:
            return 500, {
                "error": "An error occurred while fetching tax jurisdictions",
                "message": str(e),
            }

    @http_post(
        "/validate",
        response={
            200: dict,
            404: dict,
            500: dict,
        },
    )
    def validate_tax_identifier(self, request, tax_id: str, country: str):
        """Validate a tax identifier (e.g. VAT number)."""
        try:
            # Example tax ID validation - replace with actual tax service integration
            validation = {
                "valid": True,
                "tax_id": tax_id,
                "country": country,
                "business_name": "Example Business",
                "business_address": {
                    "address1": "123 Example St",
                    "city": "Example City",
                    "state": "EX",
                    "postal_code": "12345",
                    "country": country,
                },
            }
            return 200, validation
        except Exception as e:
            return 500, {
                "error": "An error occurred while validating tax identifier",
                "message": str(e),
            }
