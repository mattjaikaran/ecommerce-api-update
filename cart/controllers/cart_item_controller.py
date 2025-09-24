"""Cart item management controller with modern decorator-based approach."""

import logging
from uuid import UUID

from django.db import transaction
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
from api.exceptions import ValidationError
from cart.models import Cart, CartItem
from cart.schemas import (
    CartItemCreateSchema,
    CartItemSchema,
    CartItemUpdateSchema,
)

logger = logging.getLogger(__name__)


@api_controller("/cart-items", tags=["Cart Items"])
class CartItemController:
    """Cart item management controller with comprehensive decorators."""

    @http_get("", response={200: list[CartItemSchema]})
    @list_endpoint(
        select_related=["cart__customer__user", "product_variant__product__category"],
        prefetch_related=[
            "product_variant__options__option",
            "product_variant__options__value",
        ],
        search_fields=["product_variant__product__name", "cart__session_key"],
        filter_fields={
            "cart_id": "exact",
            "product_variant_id": "exact",
        },
        ordering_fields=["created_at", "quantity", "price"],
    )
    @search_and_filter(
        search_fields=["product_variant__product__name"],
        filter_fields={
            "cart_id": "exact",
            "product_variant_id": "exact",
        },
        ordering_fields=["created_at", "quantity"],
    )
    def list_cart_items(self, request):
        """Get all cart items with advanced filtering."""
        return 200, CartItem.objects.all()

    @http_get("/{item_id}", response={200: CartItemSchema, 404: dict})
    @detail_endpoint(
        select_related=["cart__customer__user", "product_variant__product__category"],
        prefetch_related=[
            "product_variant__options__option",
            "product_variant__options__value",
            "product_variant__product__images",
        ],
    )
    def get_cart_item(self, request, item_id: UUID):
        """Get a specific cart item by ID."""
        cart_item = get_object_or_404(CartItem, id=item_id)
        return 200, CartItemSchema.from_orm(cart_item)

    @http_post("", response={201: CartItemSchema, 400: dict})
    @create_endpoint(require_auth=False)
    @transaction.atomic
    def create_cart_item(self, request, payload: CartItemCreateSchema):
        """Create a new cart item."""
        cart = get_object_or_404(Cart, id=payload.cart_id, is_active=True)

        # Check if item already exists in cart
        existing_item = CartItem.objects.filter(
            cart=cart,
            product_variant_id=payload.product_variant_id,
        ).first()

        if existing_item:
            # Update existing item quantity
            existing_item.quantity += payload.quantity
            existing_item.save()
            cart_item = existing_item
        else:
            # Create new cart item
            cart_item = CartItem.objects.create(
                **payload.dict(),
                created_by=request.user if request.user.is_authenticated else None,
                updated_by=request.user if request.user.is_authenticated else None,
            )

        # Update cart totals
        _update_cart_totals(cart)

        return 201, CartItemSchema.from_orm(cart_item)

    @http_put("/{item_id}", response={200: CartItemSchema, 400: dict, 404: dict})
    @update_endpoint(require_auth=False)
    @transaction.atomic
    def update_cart_item(self, request, item_id: UUID, payload: CartItemUpdateSchema):
        """Update a cart item."""
        cart_item = get_object_or_404(CartItem, id=item_id)

        # Validate quantity
        if payload.quantity <= 0:
            validation_error = ValidationError("Quantity must be greater than 0")
            raise validation_error

        # Update cart item
        for field, value in payload.dict(exclude_unset=True).items():
            setattr(cart_item, field, value)

        if request.user.is_authenticated:
            cart_item.updated_by = request.user
        cart_item.save()

        # Update cart totals
        _update_cart_totals(cart_item.cart)

        return 200, CartItemSchema.from_orm(cart_item)

    @http_delete("/{item_id}", response={204: None, 404: dict})
    @delete_endpoint(require_auth=False)
    @transaction.atomic
    def delete_cart_item(self, request, item_id: UUID):
        """Delete a cart item."""
        cart_item = get_object_or_404(CartItem, id=item_id)
        cart = cart_item.cart

        cart_item.delete()

        # Update cart totals
        _update_cart_totals(cart)

        return 204, None

    @http_put(
        "/{item_id}/quantity", response={200: CartItemSchema, 400: dict, 404: dict}
    )
    @update_endpoint(require_auth=False)
    @transaction.atomic
    def update_quantity(self, request, item_id: UUID, quantity: int):
        """Update just the quantity of a cart item."""
        cart_item = get_object_or_404(CartItem, id=item_id)

        if quantity <= 0:
            validation_error = ValidationError("Quantity must be greater than 0")
            raise validation_error

        cart_item.quantity = quantity
        if request.user.is_authenticated:
            cart_item.updated_by = request.user
        cart_item.save()

        # Update cart totals
        _update_cart_totals(cart_item.cart)

        return 200, CartItemSchema.from_orm(cart_item)

    @http_post("/{item_id}/increment", response={200: CartItemSchema, 404: dict})
    @update_endpoint(require_auth=False)
    @transaction.atomic
    def increment_quantity(self, request, item_id: UUID):
        """Increment cart item quantity by 1."""
        cart_item = get_object_or_404(CartItem, id=item_id)

        cart_item.quantity += 1
        if request.user.is_authenticated:
            cart_item.updated_by = request.user
        cart_item.save()

        # Update cart totals
        _update_cart_totals(cart_item.cart)

        return 200, CartItemSchema.from_orm(cart_item)

    @http_post(
        "/{item_id}/decrement", response={200: CartItemSchema, 400: dict, 404: dict}
    )
    @update_endpoint(require_auth=False)
    @transaction.atomic
    def decrement_quantity(self, request, item_id: UUID):
        """Decrement cart item quantity by 1."""
        cart_item = get_object_or_404(CartItem, id=item_id)

        if cart_item.quantity <= 1:
            validation_error = ValidationError(
                "Cannot decrement quantity below 1. Use delete instead."
            )
            raise validation_error

        cart_item.quantity -= 1
        if request.user.is_authenticated:
            cart_item.updated_by = request.user
        cart_item.save()

        # Update cart totals
        _update_cart_totals(cart_item.cart)

        return 200, CartItemSchema.from_orm(cart_item)

    @http_get("/cart/{cart_id}", response={200: list[CartItemSchema]})
    @list_endpoint(
        require_auth=False,
        select_related=["product_variant__product__category"],
        prefetch_related=[
            "product_variant__options__option",
            "product_variant__options__value",
            "product_variant__product__images",
        ],
        ordering_fields=["created_at", "product_variant__name"],
    )
    def get_items_by_cart(self, request, cart_id: UUID):
        """Get all items for a specific cart."""
        cart = get_object_or_404(Cart, id=cart_id, is_active=True)
        return 200, cart.items.all().order_by("created_at")

    @http_get("/stats", response={200: dict})
    @detail_endpoint(cache_timeout=300)
    def get_cart_item_stats(self, request):
        """Get cart item statistics."""
        from django.db.models import Avg, Count, Sum

        stats = CartItem.objects.aggregate(
            total_items=Count("id"),
            average_quantity=Avg("quantity"),
            total_value=Sum("price"),
            unique_products=Count("product_variant", distinct=True),
        )

        return 200, stats


def _update_cart_totals(cart: Cart) -> None:
    """Update cart totals based on current items."""
    items = cart.items.all()

    subtotal = sum(item.quantity * item.price for item in items)
    total_quantity = sum(item.quantity for item in items)

    cart.subtotal = subtotal
    cart.total_price = subtotal  # Can be extended with taxes, discounts, etc.
    cart.total_quantity = total_quantity
    cart.save()
