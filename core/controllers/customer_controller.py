from typing import List
from ninja_extra import api_controller, http_get, http_post, http_put, http_delete
from ninja_extra.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from core.models import Customer
from core.schemas.customer import (
    CustomerSchema,
    CustomerCreateSchema,
    CustomerUpdateSchema,
)
import logging
from uuid import UUID

logger = logging.getLogger(__name__)


@api_controller("/customers", tags=["Customers"])
class CustomerController:
    permission_classes = [IsAuthenticated]

    @http_get("", response={200: List[CustomerSchema], 500: dict})
    def list_customers(self, request):
        """Get all customers"""
        try:
            customers = Customer.objects.all()
            return 200, [CustomerSchema.from_orm(customer) for customer in customers]
        except Exception as e:
            logger.error(f"Error listing customers: {e}")
            return 500, {
                "error": "An error occurred while listing customers",
                "message": str(e),
            }

    @http_get("/{customer_id}", response={200: CustomerSchema, 404: dict, 500: dict})
    def get_customer(self, request, customer_id: UUID):
        """Get a customer by ID"""
        try:
            customer = get_object_or_404(Customer, id=customer_id)
            return 200, CustomerSchema.from_orm(customer)
        except Customer.DoesNotExist:
            return 404, {"error": "Customer not found"}
        except Exception as e:
            logger.error(f"Error getting customer {customer_id}: {e}")
            return 500, {
                "error": "An error occurred while getting customer",
                "message": str(e),
            }

    @http_post("", response={201: CustomerSchema, 400: dict, 500: dict})
    def create_customer(self, request, payload: CustomerCreateSchema):
        """Create a new customer"""
        try:
            customer = Customer.objects.create(
                user_id=payload.user_id,
                phone=payload.phone,
                customer_group_id=payload.customer_group_id,
                meta_data=payload.meta_data,
                created_by=request.user,
            )
            return 201, CustomerSchema.from_orm(customer)
        except Exception as e:
            logger.error(f"Error creating customer: {e}")
            return 500, {
                "error": "An error occurred while creating customer",
                "message": str(e),
            }

    @http_put(
        "/{customer_id}",
        response={200: CustomerSchema, 400: dict, 404: dict, 500: dict},
    )
    def update_customer(
        self, request, customer_id: UUID, payload: CustomerUpdateSchema
    ):
        """Update a customer"""
        try:
            customer = get_object_or_404(Customer, id=customer_id)

            if payload.phone is not None:
                customer.phone = payload.phone
            if payload.customer_group_id is not None:
                customer.customer_group_id = payload.customer_group_id
            if payload.meta_data is not None:
                customer.meta_data = payload.meta_data

            customer.save()
            return 200, CustomerSchema.from_orm(customer)
        except Customer.DoesNotExist:
            return 404, {"error": "Customer not found"}
        except Exception as e:
            logger.error(f"Error updating customer {customer_id}: {e}")
            return 500, {
                "error": "An error occurred while updating customer",
                "message": str(e),
            }

    @http_delete("/{customer_id}", response={204: None, 404: dict, 500: dict})
    def delete_customer(self, customer_id: UUID):
        """Delete a customer"""
        try:
            customer = get_object_or_404(Customer, id=customer_id)
            customer.delete()
            return 204, None
        except Customer.DoesNotExist:
            return 404, {"error": "Customer not found"}
        except Exception as e:
            logger.error(f"Error deleting customer {customer_id}: {e}")
            return 500, {
                "error": "An error occurred while deleting customer",
                "message": str(e),
            }
