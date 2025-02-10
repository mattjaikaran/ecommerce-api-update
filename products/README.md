# Products App

## Overview
The Products app manages all product-related functionality including product categories, inventory tracking, pricing, and product search capabilities.

## Features
- Product Management
- Category Management
- Inventory Tracking
- Product Search & Filtering
- Image Handling
- Price Management
- Product Variants
- Product Reviews & Ratings

## Models

### Product
```python
class Product(AbstractBaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sku = models.CharField(max_length=100, unique=True)
    stock = models.IntegerField(default=0)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    
    class Meta:
        verbose_name_plural = "Products"
        ordering = ['-date_created']
```

### Category
```python
class Category(AbstractBaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name_plural = "Categories"
```

## Directory Structure
```
products/
├── __init__.py
├── admin.py
├── apps.py
├── controllers/
│   ├── __init__.py
│   ├── product_controller.py
│   └── category_controller.py
├── models.py
├── schemas/
│   ├── __init__.py
│   ├── product.py
│   └── category.py
└── tests/
    └── __init__.py
```

## Controllers

### ProductController
```python
@api_controller("/products", tags=["Products"])
class ProductController:
    @http_get("", response={200: List[ProductSchema]})
    def get_products(self, 
                    search: str = None, 
                    category_id: UUID = None,
                    min_price: float = None,
                    max_price: float = None):
        try:
            products = Product.objects.all()
            
            if search:
                products = products.filter(
                    Q(name__icontains=search) | 
                    Q(description__icontains=search)
                )
            
            if category_id:
                products = products.filter(category_id=category_id)
                
            if min_price:
                products = products.filter(price__gte=min_price)
                
            if max_price:
                products = products.filter(price__lte=max_price)
                
            return 200, products
        except Exception as e:
            logger.error(f"Error fetching products: {e}")
            return 500, {"error": "An error occurred while fetching products", "message": str(e)}
```

## Schemas

### ProductSchema
```python
class ProductSchema(Schema):
    id: UUID
    name: str
    description: str
    price: Decimal
    sku: str
    stock: int
    category_id: UUID
    date_created: datetime
    date_modified: datetime
    is_active: bool
```

### CategorySchema
```python
class CategorySchema(Schema):
    id: UUID
    name: str
    description: Optional[str]
    parent_id: Optional[UUID]
    date_created: datetime
    date_modified: datetime
    is_active: bool
```

## API Endpoints

### Products
- GET `/api/v1/products/` - List all products
- GET `/api/v1/products/{id}/` - Get product details
- POST `/api/v1/products/` - Create new product
- PUT `/api/v1/products/{id}/` - Update product
- DELETE `/api/v1/products/{id}/` - Delete product
- GET `/api/v1/products/search/` - Search products

### Categories
- GET `/api/v1/categories/` - List all categories
- GET `/api/v1/categories/{id}/` - Get category details
- POST `/api/v1/categories/` - Create new category
- PUT `/api/v1/categories/{id}/` - Update category
- DELETE `/api/v1/categories/{id}/` - Delete category

## Testing
```bash
# Run product app tests
python manage.py test products

# Run with coverage
coverage run manage.py test products
coverage report
```

## Image Handling
- Supports multiple images per product
- Automatic thumbnail generation
- Image optimization
- S3 storage integration

## Search & Filtering
- Full-text search on product name and description
- Category filtering
- Price range filtering
- Stock status filtering
- Rating filtering

## Inventory Management
- Stock tracking
- Low stock alerts
- SKU management
- Variant tracking

## Dependencies
- Django 4.2+
- Django Ninja Extra
- Pillow (for image handling)
- django-storages (for S3 integration)
- django-filter