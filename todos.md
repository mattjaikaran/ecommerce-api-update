# TODO

## Apps Structure
- [X] Core App
    - Authentication, Users, Base Models
    - Permissions and Groups
    - Settings and Configuration
- [X] Products App
    - Products, Variants, Options
    - Categories and Collections
    - Inventory Management
    - Digital Products Support
    - SEO Fields
    - Status (draft, active, archived)
    - Images
    - Reviews
    - Tags
    - Discounts
    - Tax
    - Shipping
    - Payments
- [X] Orders App
    - Orders and Line Items
    - Order Status Management
    - Order History
    - Fulfillment Tracking
- [X] Cart App
    - Shopping Cart
    - Cart Items
    - Cart Calculations
    - Abandoned Cart Recovery
- [ ] Customers App
    - Customer Profiles
    - Customer Groups
    - Customer Addresses
    - Customer Order History
- [ ] Payments App
    - Payment Methods
    - Payment Processing
    - Refunds and Chargebacks
    - Payment Gateway Integration
- [ ] Shipping App
    - Shipping Methods
    - Shipping Zones
    - Shipping Calculations
    - Shipping Labels
- [ ] Discounts App
    - Discount Rules
    - Coupons
    - Automatic Discounts
    - Gift Cards
- [ ] Tax App
    - Tax Rules
    - Tax Zones
    - Tax Calculations
    - Tax Reports
- [ ] Analytics App
    - Sales Reports
    - Customer Analytics
    - Inventory Reports
    - Performance Metrics

- should discounts be in its own app? 
- should shipping be in its own app?
- should payments be in its own app?
- should taxes be in its own app?
or be in orders app?

## Models

### Core
- [X] User Model
    - Extended Django User with e-commerce fields
- [X] Address Model
    - Support for multiple address types
- [ ] Configuration Model
    - Store settings and preferences

### Products
- [X] Product Model
    - Base product information
    - SEO fields
    - Status (draft, active, archived)
- [X] ProductVariant Model
    - SKU, barcode
    - Price, compare at price
    - Inventory tracking
- [X] ProductOption Model
    - Color, size, material etc
- [X] ProductImage Model
    - Image management
    - Alt text, position
- [X] Category Model
    - Hierarchical categories
    - SEO fields
- [X] Collection Model
    - Curated product groups
    - Automated collections

### Orders
- [X] Order Model
    - Order details
    - Status management
    - Financial details
- [X] OrderLineItem Model
    - Product variants
    - Quantities
    - Prices at time of order
- [X] FulfillmentOrder Model
    - Shipping details
    - Tracking information
- [X] OrderNote Model
    - Internal and customer notes

### Cart
- [X] Cart Model
    - Session management
    - Expiry handling
- [X] CartItem Model
    - Product variants
    - Quantities
    - Price calculations

### Customers
- [ ] Customer Model
    - Extended user profile
    - Preferences
- [ ] CustomerGroup Model
    - Segmentation
    - Special pricing
- [ ] CustomerAddress Model
    - Multiple addresses
    - Address validation

### Payments
- [ ] PaymentMethod Model
    - Payment gateway info
    - Credentials
- [ ] Transaction Model
    - Payment processing
    - Status tracking
- [ ] Refund Model
    - Refund processing
    - Status tracking

### Shipping
- [ ] ShippingZone Model
    - Geographic zones
    - Rate calculations
- [ ] ShippingMethod Model
    - Carrier settings
    - Rate rules
- [ ] ShippingRate Model
    - Price calculations
    - Conditions

### Discounts
- [ ] Discount Model
    - Discount rules
    - Validation
- [ ] Coupon Model
    - Code generation
    - Usage tracking
- [ ] GiftCard Model
    - Balance tracking
    - Usage history

### Tax
- [ ] TaxZone Model
    - Geographic tax zones
- [ ] TaxRate Model
    - Rate calculations
    - Tax categories
- [ ] TaxExemption Model
    - Customer exemptions
    - Product exemptions

## API Controllers (using django-ninja-extra)

### Core
- [X] Authentication Controller
    - JWT token management
    - Permission checking
- [X] User Controller
    - User management
    - Profile updates

### Products
- [X] Product Controller
    - CRUD operations
    - Variant management
- [X] Category Controller
    - Hierarchical management
- [X] Collection Controller
    - Collection management
    - Product assignments

### Orders
- [X] Order Controller
    - Order processing
    - Status updates
- [X] Fulfillment Controller
    - Shipping management
    - Tracking updates

### Cart
- [X] Cart Controller
    - Cart management
    - Item updates
- [X] CartCalculation Controller
    - Price calculations
    - Discount applications

### Customers
- [ ] Customer Controller
    - Profile management
    - Address management
- [ ] CustomerGroup Controller
    - Group management
    - Member assignments

### Payments
- [ ] Payment Controller
    - Payment processing
    - Refund handling
- [ ] PaymentMethod Controller
    - Method management
    - Gateway configuration

### Shipping
- [ ] ShippingZone Controller
    - Zone management
    - Rate calculations
- [ ] ShippingMethod Controller
    - Method configuration
    - Rate updates

### Discounts
- [ ] Discount Controller
    - Discount management
    - Validation rules
- [ ] Coupon Controller
    - Code management
    - Usage tracking

### Tax
- [ ] TaxZone Controller
    - Zone management
    - Rate assignments
- [ ] TaxCalculation Controller
    - Tax calculations
    - Exemption handling

## Schemas (using Pydantic)

### Core
- [X] UserSchema
- [X] AddressSchema
- [ ] ConfigurationSchema

### Products
- [X] ProductSchema
- [X] ProductVariantSchema
- [X] ProductOptionSchema
- [X] CategorySchema
- [X] CollectionSchema

### Orders
- [X] OrderSchema
- [X] OrderLineItemSchema
- [X] FulfillmentSchema
- [X] OrderNoteSchema

### Cart
- [X] CartSchema
- [X] CartItemSchema
- [X] CartCalculationSchema

### Customers
- [X] CustomerSchema
- [X] CustomerGroupSchema
- [X] CustomerAddressSchema

### Payments
- [X] PaymentMethodSchema
- [X] TransactionSchema
- [X] RefundSchema

### Shipping
- [X] ShippingZoneSchema
- [X] ShippingMethodSchema
- [X] ShippingRateSchema

### Discounts
- [ ] DiscountSchema
- [ ] CouponSchema
- [ ] GiftCardSchema

### Tax
- [ ] TaxZoneSchema
- [ ] TaxRateSchema
- [ ] TaxExemptionSchema

## Additional Tasks

### Documentation
- [ ] API Documentation using OpenAPI/Swagger
- [ ] Model Documentation
- [ ] Setup Instructions
- [ ] Deployment Guide

### Testing
- [ ] Unit Tests for Models
- [ ] Integration Tests for Controllers
- [ ] API Tests
- [ ] Performance Tests

### Development Tools
- [X] Data Seeding Scripts
- [X] Development Environment Setup
- [ ] Docker Configuration
- [ ] CI/CD Pipeline

### Security
- [X] API Authentication
- [X] Rate Limiting
- [X] Input Validation
- [ ] Data Encryption
- [ ] PCI Compliance (for payments)

### Monitoring
- [X] Error Logging
- [ ] Performance Monitoring
- [ ] Audit Logging
- [ ] Analytics Integration
