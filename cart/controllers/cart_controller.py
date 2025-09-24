"""Cart management controller with modern decorator-based approach."""

import logging
from decimal import Decimal
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
    CartCreateSchema,
    CartItemCreateSchema,
    CartItemSchema,
    CartItemUpdateSchema,
    CartSchema,
    CartUpdateSchema,
)

logger = logging.getLogger(__name__)


@api_controller("/carts", tags=["Carts"])
class CartController:
    """Cart management controller with comprehensive decorators."""

    @http_get("", response={200: list[CartSchema]})
    @list_endpoint(
        select_related=["customer__user"],
        prefetch_related=["items__product_variant__product"],
        search_fields=[
            "session_key",
            "customer__user__username",
            "customer__user__email",
        ],
        filter_fields={
            "is_active": "boolean",
            "customer_id": "exact",
        },
        ordering_fields=["created_at", "updated_at", "total_price"],
    )
    @search_and_filter(
        search_fields=["session_key", "customer__user__username"],
        filter_fields={
            "is_active": "boolean",
            "customer_id": "exact",
        },
        ordering_fields=["created_at", "updated_at"],
    )
    def list_carts(self, request):
        """Get all carts with advanced filtering."""
        return 200, Cart.objects.filter(is_active=True)

    @http_get("/{cart_id}", response={200: CartSchema, 404: dict})
    @detail_endpoint(
        select_related=["customer__user"],
        prefetch_related=[
            "items__product_variant__product__category",
            "items__product_variant__options__option",
            "items__product_variant__options__value",
        ],
    )
    def get_cart(self, request, cart_id: UUID):
        """Get a specific cart by ID with all items."""
        cart = get_object_or_404(Cart, id=cart_id, is_active=True)
        return 200, CartSchema.from_orm(cart)

    @http_post("", response={201: CartSchema, 400: dict})
    @create_endpoint(require_auth=False)
    @transaction.atomic
    def create_cart(self, request, payload: CartCreateSchema):
        """Create a new cart."""
        cart = Cart.objects.create(
            **payload.dict(),
            created_by=request.user if request.user.is_authenticated else None,
            updated_by=request.user if request.user.is_authenticated else None,
        )
        return 201, CartSchema.from_orm(cart)

    @http_put("/{cart_id}", response={200: CartSchema, 400: dict, 404: dict})
    @update_endpoint(require_auth=False)
    @transaction.atomic
    def update_cart(self, request, cart_id: UUID, payload: CartUpdateSchema):
        """Update cart information."""
        cart = get_object_or_404(Cart, id=cart_id)

        for field, value in payload.dict(exclude_unset=True).items():
            setattr(cart, field, value)

        if request.user.is_authenticated:
            cart.updated_by = request.user

        cart.save()
        return 200, CartSchema.from_orm(cart)

    @http_delete("/{cart_id}", response={204: None, 404: dict})
    @delete_endpoint(require_auth=False)
    def delete_cart(self, request, cart_id: UUID):
        """Delete a cart."""
        cart = get_object_or_404(Cart, id=cart_id)
        cart.delete()
        return 204, None

    @http_get("/{cart_id}/items", response={200: list[CartItemSchema]})
    @list_endpoint(
        require_auth=False,
        select_related=["cart", "product_variant__product"],
        prefetch_related=[
            "product_variant__options__option",
            "product_variant__options__value",
        ],
        ordering_fields=["created_at", "product_variant__name"],
    )
    def get_cart_items(self, request, cart_id: UUID):
        """Get all items in a cart."""
        cart = get_object_or_404(Cart, id=cart_id, is_active=True)
        return 200, cart.items.all().order_by("created_at")

    @http_post("/{cart_id}/items", response={201: CartItemSchema, 400: dict, 404: dict})
    @create_endpoint(require_auth=False)
    @transaction.atomic
    def add_cart_item(self, request, cart_id: UUID, payload: CartItemCreateSchema):
        """Add an item to the cart."""
        cart = get_object_or_404(Cart, id=cart_id, is_active=True)

        # Check if item already exists in cart
        existing_item = cart.items.filter(
            product_variant_id=payload.product_variant_id
        ).first()

        if existing_item:
            # Update quantity
            existing_item.quantity += payload.quantity
            existing_item.save()
            cart_item = existing_item
        else:
            # Create new item
            cart_item = CartItem.objects.create(
                cart=cart,
                **payload.dict(),
                created_by=request.user if request.user.is_authenticated else None,
                updated_by=request.user if request.user.is_authenticated else None,
            )

        # Update cart totals
        _update_cart_totals(cart)

        return 201, CartItemSchema.from_orm(cart_item)

    @http_put(
        "/{cart_id}/items/{item_id}",
        response={200: CartItemSchema, 400: dict, 404: dict},
    )
    @update_endpoint(require_auth=False)
    @transaction.atomic
    def update_cart_item(
        self, request, cart_id: UUID, item_id: UUID, payload: CartItemUpdateSchema
    ):
        """Update a cart item."""
        cart = get_object_or_404(Cart, id=cart_id, is_active=True)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)

        # Validate quantity
        if payload.quantity <= 0:
            validation_error = ValidationError("Quantity must be greater than 0")
            raise validation_error

        cart_item.quantity = payload.quantity
        if request.user.is_authenticated:
            cart_item.updated_by = request.user
        cart_item.save()

        # Update cart totals
        _update_cart_totals(cart)

        return 200, CartItemSchema.from_orm(cart_item)

    @http_delete("/{cart_id}/items/{item_id}", response={204: None, 404: dict})
    @delete_endpoint(require_auth=False)
    @transaction.atomic
    def remove_cart_item(self, request, cart_id: UUID, item_id: UUID):
        """Remove an item from the cart."""
        cart = get_object_or_404(Cart, id=cart_id, is_active=True)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)

        cart_item.delete()

        # Update cart totals
        _update_cart_totals(cart)

        return 204, None

    @http_post("/{cart_id}/clear", response={200: CartSchema, 404: dict})
    @update_endpoint(require_auth=False)
    @transaction.atomic
    def clear_cart(self, request, cart_id: UUID):
        """Clear all items from the cart."""
        cart = get_object_or_404(Cart, id=cart_id, is_active=True)

        cart.items.all().delete()

        # Reset cart totals
        cart.subtotal = Decimal("0.00")
        cart.total_price = Decimal("0.00")
        cart.total_quantity = 0
        cart.save()

        return 200, CartSchema.from_orm(cart)

    @http_get("/session/{session_key}", response={200: CartSchema, 404: dict})
    @detail_endpoint(
        require_auth=False,
        cache_timeout=60,
        select_related=["customer__user"],
        prefetch_related=["items__product_variant__product"],
    )
    def get_cart_by_session(self, request, session_key: str):
        """Get a cart by session key."""
        cart = get_object_or_404(Cart, session_key=session_key, is_active=True)
        return 200, CartSchema.from_orm(cart)

    @http_get("/customer/{customer_id}", response={200: list[CartSchema]})
    @list_endpoint(
        select_related=["customer__user"],
        prefetch_related=["items__product_variant__product"],
        filter_fields={"is_active": "boolean"},
        ordering_fields=["created_at", "updated_at"],
    )
    def get_customer_carts(self, request, customer_id: UUID):
        """Get all carts for a specific customer."""
        return 200, Cart.objects.filter(customer_id=customer_id, is_active=True)

    @http_post(
        "/{cart_id}/merge/{source_cart_id}",
        response={200: CartSchema, 400: dict, 404: dict},
    )
    @update_endpoint(require_auth=False)
    @transaction.atomic
    def merge_carts(self, request, cart_id: UUID, source_cart_id: UUID):
        """Merge two carts together."""
        target_cart = get_object_or_404(Cart, id=cart_id, is_active=True)
        source_cart = get_object_or_404(Cart, id=source_cart_id, is_active=True)

        if target_cart.id == source_cart.id:
            validation_error = ValidationError("Cannot merge cart with itself")
            raise validation_error

        # Move items from source cart to target cart
        for source_item in source_cart.items.all():
            existing_item = target_cart.items.filter(
                product_variant=source_item.product_variant
            ).first()

            if existing_item:
                # Merge quantities
                existing_item.quantity += source_item.quantity
                existing_item.save()
            else:
                # Move item to target cart
                source_item.cart = target_cart
                source_item.save()

        # Delete source cart
        source_cart.delete()

        # Update target cart totals
        _update_cart_totals(target_cart)

        return 200, CartSchema.from_orm(target_cart)


def _update_cart_totals(cart: Cart) -> None:
    """Update cart totals based on current items."""
    items = cart.items.all()

    subtotal = sum(item.quantity * item.price for item in items)
    total_quantity = sum(item.quantity for item in items)

    cart.subtotal = subtotal
    cart.total_price = subtotal  # Can be extended with taxes, discounts, etc.
    cart.total_quantity = total_quantity
    cart.save()
