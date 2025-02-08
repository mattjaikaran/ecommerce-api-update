import logging
from ninja_extra import api_controller, http_get, http_post, http_put, http_delete
from cart.models import Cart
from cart.schemas import CartSchema

logger = logging.getLogger(__name__)


@api_controller("/cart", tags=["Cart"])
class CartController:
    @http_get("/", response={200: CartSchema, 404: dict, 500: dict})
    def get_cart(self, request):
        try:
            cart = Cart.objects.get(user=request.user)
            return 200, cart
        except Cart.DoesNotExist:
            return 404, {"message": "Cart not found"}
        except Exception as e:
            logger.error(f"Error getting cart: {str(e)}")
            return 500, {
                "message": "Internal server error - get_cart",
                "error": str(e),
            }

    @http_post("/", response={201: CartSchema, 500: dict})
    def create_cart(self, request):
        try:
            cart = Cart.objects.create(user=request.user)
            return 201, cart
        except Exception as e:
            logger.error(f"Error creating cart: {str(e)}")
            return 500, {
                "message": "Internal server error - create_cart",
                "error": str(e),
            }

    @http_put("/", response={200: CartSchema, 404: dict, 500: dict})
    def update_cart(self, request):
        try:
            cart = Cart.objects.get(user=request.user)
            cart.items.set(request.validated_data.get("items", []))
            cart.save()
            return 200, cart
        except Exception as e:
            logger.error(f"Error updating cart: {str(e)}")
            return 500, {
                "message": "Internal server error - update_cart",
                "error": str(e),
            }

    @http_delete("/", response={204: dict, 404: dict, 500: dict})
    def delete_cart(self, request):
        try:
            cart = Cart.objects.get(user=request.user)
            cart.delete()
            return 204, {}
        except Cart.DoesNotExist:
            return 404, {"message": "Cart not found"}
        except Exception as e:
            logger.error(f"Error deleting cart: {str(e)}")
            return 500, {
                "message": "Internal server error - delete_cart",
                "error": str(e),
            }
