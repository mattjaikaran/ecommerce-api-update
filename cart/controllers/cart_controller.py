import logging
from ninja_extra import api_controller, http_get, http_post, http_put, http_delete
from cart.models import Cart
from cart.schemas import CartSchema
from core.models import Customer
from django.contrib.auth.models import AnonymousUser
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)


@api_controller("/cart", tags=["Cart"])
class CartController:
    @http_get("", response={200: CartSchema, 404: dict, 500: dict})
    def get_cart(self, request):
        """Get the current user's cart"""
        try:
            if isinstance(request.user, AnonymousUser):
                # Return empty cart schema for anonymous users
                return 200, CartSchema(
                    id=uuid.uuid4(),  # Generate a temporary UUID for anonymous cart
                    items=[],
                    subtotal=0.0,
                    total_price=0.0,
                    total_quantity=0,
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                )

            # Get customer from authenticated user
            customer = Customer.objects.get(user=request.user)
            # Get or create cart for customer
            cart, created = Cart.objects.get_or_create(
                customer=customer, is_active=True, defaults={"created_by": request.user}
            )
            return 200, cart
        except Customer.DoesNotExist:
            return 404, {"message": "Customer profile not found"}
        except Exception as e:
            logger.error(f"Error getting cart: {str(e)}")
            return 500, {
                "message": "Internal server error - get_cart",
                "error": str(e),
            }

    @http_post("", response={201: CartSchema, 400: dict, 404: dict, 500: dict})
    def create_cart(self, request):
        """Create a new cart for the current user"""
        try:
            if isinstance(request.user, AnonymousUser):
                return 400, {"message": "Must be logged in to create a cart"}

            # Get customer from authenticated user
            customer = Customer.objects.get(user=request.user)
            # Check if active cart exists
            if Cart.objects.filter(customer=customer, is_active=True).exists():
                return 400, {"message": "Active cart already exists"}
            # Create new cart
            cart = Cart.objects.create(customer=customer, created_by=request.user)
            return 201, cart
        except Customer.DoesNotExist:
            return 404, {"message": "Customer profile not found"}
        except Exception as e:
            logger.error(f"Error creating cart: {str(e)}")
            return 500, {
                "message": "Internal server error - create_cart",
                "error": str(e),
            }

    @http_put("", response={200: CartSchema, 400: dict, 404: dict, 500: dict})
    def update_cart(self, request):
        """Update the current user's cart"""
        try:
            if isinstance(request.user, AnonymousUser):
                return 400, {"message": "Must be logged in to update cart"}

            customer = Customer.objects.get(user=request.user)
            cart = Cart.objects.get(customer=customer, is_active=True)
            cart.items.set(request.validated_data.get("items", []))
            cart.save()
            return 200, cart
        except (Customer.DoesNotExist, Cart.DoesNotExist):
            return 404, {"message": "Cart not found"}
        except Exception as e:
            logger.error(f"Error updating cart: {str(e)}")
            return 500, {
                "message": "Internal server error - update_cart",
                "error": str(e),
            }

    @http_delete("", response={204: dict, 400: dict, 404: dict, 500: dict})
    def delete_cart(self, request):
        """Delete the current user's cart"""
        try:
            if isinstance(request.user, AnonymousUser):
                return 400, {"message": "Must be logged in to delete cart"}

            # Get customer from authenticated user
            customer = Customer.objects.get(user=request.user)
            # Get active cart
            cart = Cart.objects.get(customer=customer, is_active=True)
            cart.is_active = False
            cart.save()
            return 204, {"message": "Cart deactivated successfully"}
        except Customer.DoesNotExist:
            return 404, {"message": "Customer profile not found"}
        except Cart.DoesNotExist:
            return 404, {"message": "Active cart not found"}
        except Exception as e:
            logger.error(f"Error deleting cart: {str(e)}")
            return 500, {
                "message": "Internal server error - delete_cart",
                "error": str(e),
            }
