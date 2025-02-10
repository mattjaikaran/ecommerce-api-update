# Cart App

## Overview
The Cart app manages shopping cart functionality, including cart creation, item management, price calculations, and cart-to-order conversion.

## Features
- Cart Management
- Cart Item Management
- Price Calculations
- Cart Session Management
- Cart Merging
- Cart Expiration
- Cart Recovery
- Cart Analytics

## Models

### Cart
```python
class Cart(AbstractBaseModel):
    user = models.ForeignKey('core.User', null=True, blank=True, on_delete=models.CASCADE)
    session_id = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(
        max_length=50,
        choices=CartStatus.choices,
        default=CartStatus.ACTIVE
    )
    expires_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Carts"
        ordering = ['-date_created']
```

### CartItem
```python
class CartItem(AbstractBaseModel):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    class Meta:
        verbose_name_plural = "Cart Items"
        unique_together = ('cart', 'product')
```

## Directory Structure
```
cart/
├── __init__.py
├── admin.py
├── apps.py
├── controllers/
│   ├── __init__.py
│   ├── cart_controller.py
│   └── cart_item_controller.py
├── models.py
├── schemas/
│   ├── __init__.py
│   └── cart.py
└── tests/
    └── __init__.py
```

## Controllers

### CartController
```python
@api_controller("/cart", tags=["Cart"])
class CartController:
    @http_get("", response={200: CartSchema})
    def get_cart(self, request):
        try:
            cart = self._get_or_create_cart(request)
            return 200, cart
        except Exception as e:
            logger.error(f"Error fetching cart: {e}")
            return 500, {"error": "An error occurred while fetching cart", "message": str(e)}
    
    def _get_or_create_cart(self, request):
        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user, status=CartStatus.ACTIVE).first()
            if not cart:
                cart = Cart.objects.create(user=request.user)
        else:
            session_id = request.session.session_key or request.session.create()
            cart = Cart.objects.filter(session_id=session_id, status=CartStatus.ACTIVE).first()
            if not cart:
                cart = Cart.objects.create(session_id=session_id)
        return cart
```

### CartItemController
```python
@api_controller("/cart/items", tags=["Cart Items"])
class CartItemController:
    @http_post("", response={201: CartItemSchema})
    def add_item(self, request, product_id: UUID, quantity: int = 1):
        try:
            cart = self._get_or_create_cart(request)
            product = Product.objects.get(id=product_id)
            
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={'quantity': quantity}
            )
            
            if not created:
                cart_item.quantity += quantity
                cart_item.save()
                
            return 201, cart_item
        except Exception as e:
            logger.error(f"Error adding item to cart: {e}")
            return 500, {"error": "An error occurred while adding item to cart", "message": str(e)}
```

## Schemas

### CartSchema
```python
class CartSchema(Schema):
    id: UUID
    user_id: Optional[UUID]
    session_id: Optional[str]
    status: str
    expires_at: Optional[datetime]
    date_created: datetime
    date_modified: datetime
    items: List[CartItemSchema]
    total: Decimal
```

### CartItemSchema
```python
class CartItemSchema(Schema):
    id: UUID
    product_id: UUID
    quantity: int
    date_created: datetime
    date_modified: datetime
    subtotal: Decimal
```

## API Endpoints

### Cart
- GET `/api/v1/cart/` - Get current cart
- POST `/api/v1/cart/merge/` - Merge guest cart with user cart
- DELETE `/api/v1/cart/` - Clear cart
- GET `/api/v1/cart/total/` - Get cart total

### Cart Items
- GET `/api/v1/cart/items/` - List cart items
- POST `/api/v1/cart/items/` - Add item to cart
- PUT `/api/v1/cart/items/{id}/` - Update cart item
- DELETE `/api/v1/cart/items/{id}/` - Remove item from cart
- POST `/api/v1/cart/items/bulk/` - Bulk add items

## Cart Statuses
```python
class CartStatus(models.TextChoices):
    ACTIVE = 'active', 'Active'
    MERGED = 'merged', 'Merged'
    CONVERTED = 'converted', 'Converted to Order'
    ABANDONED = 'abandoned', 'Abandoned'
```

## Testing
```bash
# Run cart app tests
python manage.py test cart

# Run with coverage
coverage run manage.py test cart
coverage report
```

## Cart Lifecycle
1. Cart Creation
   - User authentication check
   - Session management
   - Expiration setup
2. Item Management
   - Add/update/remove items
   - Quantity validation
   - Stock checking
3. Cart Merging
   - Guest to user cart transfer
   - Duplicate item handling
4. Cart Recovery
   - Abandoned cart detection
   - Recovery email triggers
   - Recovery analytics

## Price Calculations
- Product base price
- Quantity adjustments
- Applied discounts
- Tax calculations
- Shipping estimates

## Dependencies
- Django 4.2+
- Django Ninja Extra
- Redis (for session storage)
- Celery (for background tasks) 