import logging
from uuid import UUID

from django.shortcuts import get_object_or_404
from ninja_extra import api_controller, http_delete, http_get, http_post, http_put

from cart.models import Cart, CartItem
from cart.schemas import CartItemCreateSchema, CartItemSchema, CartItemUpdateSchema
from core.models import Customer
from products.models import ProductVariant

logger = logging.getLogger(__name__)


@api_controller("/cart", tags=["Cart Items"])
class CartItemController:
    @http_get("/items", response={200: list[CartItemSchema], 404: dict, 500: dict})
    def list_cart_items(self, request):
        """List all items in the current user's cart"""
        try:
            # Return empty list for anonymous users
            if not request.user.is_authenticated:
                return 200, []

            # Get customer's active cart
            try:
                customer = Customer.objects.get(user=request.user)
                cart = Cart.objects.get(customer=customer, is_active=True)
                cart_items = CartItem.objects.filter(cart=cart)
                return 200, [CartItemSchema.from_orm(item) for item in cart_items]
            except (Customer.DoesNotExist, Cart.DoesNotExist):
                # Return empty list if no customer or active cart exists
                return 200, []

        except Exception as e:
            logger.error(f"Error listing cart items: {e!s}")
            return 500, {
                "message": "Internal server error - list_cart_items",
                "error": str(e),
            }

    @http_post(
        "/items", response={201: CartItemSchema, 400: dict, 404: dict, 500: dict}
    )
    def create_cart_item(self, request, payload: CartItemCreateSchema):
        """Add an item to the current user's cart"""
        try:
            # Get customer's active cart
            customer = Customer.objects.get(user=request.user)
            cart = Cart.objects.get(customer=customer, is_active=True)

            # Get product variant
            variant = get_object_or_404(ProductVariant, id=payload.product_variant_id)

            # Check if item already exists in cart
            existing_item = CartItem.objects.filter(
                cart=cart, product_variant=variant
            ).first()

            if existing_item:
                # Update quantity if item exists
                existing_item.quantity += payload.quantity
                existing_item.save()
                cart_item = existing_item
            else:
                # Create new cart item
                cart_item = CartItem.objects.create(
                    cart=cart,
                    product_variant=variant,
                    quantity=payload.quantity,
                    price=variant.price,
                    created_by=request.user,
                )

            # Update cart totals
            self._update_cart_totals(cart)

            return 201, cart_item
        except Customer.DoesNotExist:
            return 404, {"message": "Customer profile not found"}
        except Cart.DoesNotExist:
            return 404, {"message": "Active cart not found"}
        except ProductVariant.DoesNotExist:
            return 404, {"message": "Product variant not found"}
        except Exception as e:
            logger.error(f"Error creating cart item: {e!s}")
            return 500, {
                "message": "Internal server error - create_cart_item",
                "error": str(e),
            }

    @http_put(
        "/items/{item_id}",
        response={200: CartItemSchema, 400: dict, 404: dict, 500: dict},
    )
    def update_cart_item(self, request, item_id: UUID, payload: CartItemUpdateSchema):
        """Update a cart item's quantity"""
        try:
            # Get customer's active cart
            customer = Customer.objects.get(user=request.user)
            cart = Cart.objects.get(customer=customer, is_active=True)

            # Get cart item
            cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)

            # Update quantity
            cart_item.quantity = payload.quantity
            cart_item.save()

            # Update cart totals
            self._update_cart_totals(cart)

            return 200, cart_item
        except Customer.DoesNotExist:
            return 404, {"message": "Customer profile not found"}
        except Cart.DoesNotExist:
            return 404, {"message": "Active cart not found"}
        except CartItem.DoesNotExist:
            return 404, {"message": "Cart item not found"}
        except Exception as e:
            logger.error(f"Error updating cart item: {e!s}")
            return 500, {
                "message": "Internal server error - update_cart_item",
                "error": str(e),
            }

    @http_delete("/items/{item_id}", response={204: dict, 404: dict, 500: dict})
    def delete_cart_item(self, request, item_id: UUID):
        """Remove an item from the cart"""
        try:
            # Get customer's active cart
            customer = Customer.objects.get(user=request.user)
            cart = Cart.objects.get(customer=customer, is_active=True)

            # Get and delete cart item
            cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
            cart_item.delete()

            # Update cart totals
            self._update_cart_totals(cart)

            return 204, {"message": "Cart item deleted successfully"}
        except Customer.DoesNotExist:
            return 404, {"message": "Customer profile not found"}
        except Cart.DoesNotExist:
            return 404, {"message": "Active cart not found"}
        except CartItem.DoesNotExist:
            return 404, {"message": "Cart item not found"}
        except Exception as e:
            logger.error(f"Error deleting cart item: {e!s}")
            return 500, {
                "message": "Internal server error - delete_cart_item",
                "error": str(e),
            }

    def _update_cart_totals(self, cart: Cart):
        """Update cart totals based on items"""
        cart_items = CartItem.objects.filter(cart=cart)
        subtotal = sum(item.price * item.quantity for item in cart_items)
        total_quantity = sum(item.quantity for item in cart_items)

        cart.subtotal = subtotal
        cart.total_price = subtotal  # Add tax/shipping calculation if needed
        cart.total_quantity = total_quantity
        cart.save()
