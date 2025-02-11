# Orders App

## Overview
The Orders app manages the entire order lifecycle, from creation to fulfillment, including payment processing, order status tracking, and shipping integration.

## Features
- Order Management
- Order Status Tracking
- Payment Processing
- Shipping Integration
- Order History
- Order Items Management
- Order Fulfillment
- Invoice Generation
- Email Notifications

## Models

### Order
```python
class Order(AbstractBaseModel):
    user = models.ForeignKey('core.User', on_delete=models.CASCADE)
    status = models.CharField(
        max_length=50,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING
    )
    total = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.ForeignKey('ShippingAddress', on_delete=models.PROTECT)
    payment_status = models.CharField(
        max_length=50,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING
    )
    tracking_number = models.CharField(max_length=100, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Orders"
        ordering = ['-created_at']
```

### OrderItem
```python
class OrderItem(AbstractBaseModel):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name_plural = "Order Items"
```

### ShippingAddress
```python
class ShippingAddress(AbstractBaseModel):
    user = models.ForeignKey('core.User', on_delete=models.CASCADE)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    
    class Meta:
        verbose_name_plural = "Shipping Addresses"
```

## Directory Structure
```
orders/
├── __init__.py
├── admin.py
├── apps.py
├── controllers/
│   ├── __init__.py
│   ├── order_controller.py
│   └── fulfillment_controller.py
├── models.py
├── schemas/
│   ├── __init__.py
│   ├── order.py
│   └── shipping.py
└── tests/
    └── __init__.py
```

## Controllers

### OrderController
```python
@api_controller("/orders", tags=["Orders"])
class OrderController:
    @http_get("", response={200: List[OrderSchema]})
    def get_orders(self, user_id: UUID = None, status: str = None):
        try:
            orders = Order.objects.all()
            
            if user_id:
                orders = orders.filter(user_id=user_id)
                
            if status:
                orders = orders.filter(status=status)
                
            return 200, orders
        except Exception as e:
            logger.error(f"Error fetching orders: {e}")
            return 500, {"error": "An error occurred while fetching orders", "message": str(e)}
```

## Schemas

### OrderSchema
```python
class OrderSchema(Schema):
    id: UUID
    user_id: UUID
    status: str
    total: Decimal
    shipping_address_id: UUID
    payment_status: str
    tracking_number: Optional[str]
    notes: Optional[str]
    created_at: datetime
    date_modified: datetime
    items: List[OrderItemSchema]
```

### OrderItemSchema
```python
class OrderItemSchema(Schema):
    id: UUID
    product_id: UUID
    quantity: int
    price: Decimal
    created_at: datetime
    date_modified: datetime
```

## API Endpoints

### Orders
- GET `/api/v1/orders/` - List all orders
- GET `/api/v1/orders/{id}/` - Get order details
- POST `/api/v1/orders/` - Create new order
- PUT `/api/v1/orders/{id}/` - Update order
- DELETE `/api/v1/orders/{id}/` - Cancel order
- GET `/api/v1/orders/user/{user_id}/` - Get user orders

### Fulfillment
- PUT `/api/v1/orders/{id}/fulfill/` - Mark order as fulfilled
- PUT `/api/v1/orders/{id}/ship/` - Update shipping information
- GET `/api/v1/orders/{id}/tracking/` - Get tracking information

### Shipping
- GET `/api/v1/shipping/addresses/` - List shipping addresses
- POST `/api/v1/shipping/addresses/` - Create shipping address
- PUT `/api/v1/shipping/addresses/{id}/` - Update shipping address
- DELETE `/api/v1/shipping/addresses/{id}/` - Delete shipping address

## Order Statuses
```python
class OrderStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    PROCESSING = 'processing', 'Processing'
    SHIPPED = 'shipped', 'Shipped'
    DELIVERED = 'delivered', 'Delivered'
    CANCELLED = 'cancelled', 'Cancelled'
```

## Payment Statuses
```python
class PaymentStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    PAID = 'paid', 'Paid'
    FAILED = 'failed', 'Failed'
    REFUNDED = 'refunded', 'Refunded'
```

## Testing
```bash
# Run orders app tests
python manage.py test orders

# Run with coverage
coverage run manage.py test orders
coverage report
```

## Order Lifecycle
1. Order Creation
   - Cart conversion to order
   - Address validation
   - Stock verification
2. Payment Processing
   - Payment gateway integration
   - Payment verification
3. Order Fulfillment
   - Stock reduction
   - Shipping label generation
   - Tracking number assignment
4. Order Completion
   - Delivery confirmation
   - Customer notification
   - Review invitation

## Dependencies
- Django 4.2+
- Django Ninja Extra
- Stripe (for payments)
- django-shipping (for shipping integration)
- WeasyPrint (for PDF generation)
