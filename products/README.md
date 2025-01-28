# Products App

A comprehensive product management system for e-commerce.

## Features

- Complete product management with variants and options
- Hierarchical category system
- Collections for product grouping
- Product reviews and ratings
- Product tagging
- SEO optimization
- Digital product support
- Inventory tracking
- Tax and shipping class management

## Models

### Product
- Base product information
- SEO fields
- Status (draft, active, archived)
- Digital product support
- Tax and shipping classes
- Inventory tracking
- Dimensions and weight
- Price management (regular, compare at, cost)
- Meta data support

### ProductVariant
- SKU and barcode
- Price management
- Inventory tracking
- Dimensions and weight
- Option combinations
- Meta data support

### ProductOption & ProductOptionValue
- Configurable product options (e.g., size, color)
- Option values with position ordering
- Support for variant combinations

### ProductCategory
- Hierarchical categories
- SEO optimization
- Image support
- Position ordering

### ProductCollection
- Curated product groups
- SEO optimization
- Image support
- Position ordering

### ProductReview
- Rating system (1-5 stars)
- Verified reviews
- Featured reviews
- User authentication
- Title and comment support

### ProductTag
- Product tagging system
- Slug support
- Description fields

### ProductImage
- Image management for products and variants
- Alt text support
- Position ordering

## API Endpoints

### Products (`/api/products/`)
- `GET /` - List all products
- `GET /{id}` - Get product details
- `POST /` - Create product
- `PUT /{id}` - Update product
- `DELETE /{id}` - Delete product

### Product Variants (`/api/products/{product_id}/variants/`)
- `GET /` - List variants
- `GET /{id}` - Get variant details
- `POST /` - Create variant
- `PUT /{id}` - Update variant
- `DELETE /{id}` - Delete variant

### Categories (`/api/categories/`)
- `GET /` - List categories
- `GET /{id}` - Get category details
- `POST /` - Create category
- `PUT /{id}` - Update category
- `DELETE /{id}` - Delete category
- `GET /tree` - Get category tree

### Options (`/api/options/`)
- `GET /` - List options
- `GET /{id}` - Get option details
- `POST /` - Create option
- `PUT /{id}` - Update option
- `DELETE /{id}` - Delete option

### Collections (`/api/collections/`)
- `GET /` - List collections
- `GET /{id}` - Get collection details
- `POST /` - Create collection
- `PUT /{id}` - Update collection
- `DELETE /{id}` - Delete collection
- `POST /{id}/products/{product_id}` - Add product to collection
- `DELETE /{id}/products/{product_id}` - Remove product from collection
- `POST /{id}/products` - Bulk add products
- `DELETE /{id}/products` - Bulk remove products

### Reviews (`/api/reviews/`)
- `GET /` - List reviews
- `GET /{id}` - Get review details
- `GET /products/{product_id}` - Get product reviews
- `POST /` - Create review
- `PUT /{id}` - Update review
- `DELETE /{id}` - Delete review
- `PUT /{id}/verify` - Verify review (admin only)
- `PUT /{id}/feature` - Feature/unfeature review (admin only)

### Tags (`/api/tags/`)
- `GET /` - List tags
- `GET /{id}` - Get tag details
- `POST /` - Create tag
- `PUT /{id}` - Update tag
- `DELETE /{id}` - Delete tag
- `POST /{id}/products/{product_id}` - Add product to tag
- `DELETE /{id}/products/{product_id}` - Remove product from tag
- `POST /{id}/products` - Bulk add products
- `DELETE /{id}/products` - Bulk remove products

## Authentication

All endpoints require authentication using JWT tokens. Include the token in the Authorization header:
```
Authorization: Bearer <token>
```

## Error Handling

All endpoints follow a consistent error response format:
```json
{
    "error": "Error message",
    "message": "Detailed error message"
}
```

Common status codes:
- 200: Success
- 201: Created
- 204: Deleted
- 400: Validation error
- 401: Unauthorized
- 403: Forbidden
- 404: Not found
- 500: Server error

## Database Optimization

- Uses select_related and prefetch_related for efficient queries
- Proper indexing on frequently queried fields
- Transaction management for data integrity
- Optimistic locking for concurrent updates


