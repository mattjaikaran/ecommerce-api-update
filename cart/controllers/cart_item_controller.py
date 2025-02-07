import logging
from typing import List
from ninja_extra import api_controller, http_get, http_post, http_put, http_delete
from cart.models import CartItem
from cart.schemas import CartItemSchema

logger = logging.getLogger(__name__)


@api_controller("/cart", tags=["Cart"])
class CartItemController:
    @http_get("/items", response={200: List[CartItemSchema], 500: dict})
    def list_cart_items(self, request):
        try:
            cart_items = CartItem.objects.filter(cart=request.user.cart)
            return 200, cart_items
        except Exception as e:
            logger.error(f"Error listing cart items: {str(e)}")
            return 500, {
                "message": "Internal server error - list_cart_items",
                "error": str(e),
            }

    @http_post("/items", response={201: CartItemSchema, 500: dict})
    def create_cart_item(self, request):
        try:
            cart_item = CartItem.objects.create(**request.validated_data)
            return 201, cart_item
        except Exception as e:
            logger.error(f"Error creating cart item: {str(e)}")
            return 500, {
                "message": "Internal server error - create_cart_item",
                "error": str(e),
            }

    @http_get("/items/{item_id}", response={200: CartItemSchema, 404: dict, 500: dict})
    def get_cart_item(self, request, item_id: int):
        try:
            cart_item = CartItem.objects.get(id=item_id)
            return 200, cart_item
        except CartItem.DoesNotExist:
            return 404, {"message": "Cart item not found"}
        except Exception as e:
            logger.error(f"Error getting cart item: {str(e)}")
            return 500, {
                "message": "Internal server error - get_cart_item",
                "error": str(e),
            }

    @http_put("/items/{item_id}", response={200: CartItemSchema, 404: dict, 500: dict})
    def update_cart_item(self, request, item_id: int):
        try:
            cart_item = CartItem.objects.get(id=item_id)
            cart_item.quantity = request.validated_data.get(
                "quantity", cart_item.quantity
            )
            cart_item.save()
            return 200, cart_item
        except CartItem.DoesNotExist:
            return 404, {"message": "Cart item not found"}
        except Exception as e:
            logger.error(f"Error updating cart item: {str(e)}")
            return 500, {
                "message": "Internal server error - update_cart_item",
                "error": str(e),
            }

    @http_delete("/items/{item_id}", response={204: dict, 404: dict, 500: dict})
    def delete_cart_item(self, request, item_id: int):
        try:
            cart_item = CartItem.objects.get(id=item_id)
            cart_item.delete()
            return 204, {}
        except CartItem.DoesNotExist:
            return 404, {"message": "Cart item not found"}
        except Exception as e:
            logger.error(f"Error deleting cart item: {str(e)}")
            return 500, {
                "message": "Internal server error - delete_cart_item",
                "error": str(e),
            }
