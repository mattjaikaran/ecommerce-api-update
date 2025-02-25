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
- [X] Customers App
    - Customer Profiles
    - Customer Groups
    - Customer Addresses
    - Customer Order History
- [X] Payments App
    - Payment Methods
    - Payment Processing
    - Refunds and Chargebacks
    - Payment Gateway Integration
- [X] Shipping App
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

## Models

### Core
- [X] User Model
    - Extended Django User with e-commerce fields
- [X] Address Model
    - Support for multiple address types
- [X] Configuration Model
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
- [X] Customer Model
    - Extended user profile
    - Preferences
- [X] CustomerGroup Model
    - Segmentation
    - Special pricing
- [X] CustomerAddress Model
    - Multiple addresses
    - Address validation

### Payments
- [X] PaymentMethod Model
    - Payment gateway info
    - Credentials
- [X] Transaction Model
    - Payment processing
    - Status tracking
- [X] Refund Model
    - Refund processing
    - Status tracking

### Shipping
- [X] ShippingZone Model
    - Geographic zones
    - Rate calculations
- [X] ShippingMethod Model
    - Carrier settings
    - Rate rules
- [X] ShippingRate Model
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
- [X] TaxZone Model
    - Geographic tax zones
- [X] TaxRate Model
    - Rate calculations
    - Tax categories
- [X] TaxExemption Model
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
- [X] Customer Controller
    - Customer profile management
    - Address management

### Products
- [X] Product Controller
    - CRUD operations
    - Variant management
- [X] Category Controller
    - Hierarchical management
- [X] Collection Controller
    - Collection management
    - Product assignments
- [X] Tag Controller
    - Tag management
- [X] ProductOption Controller
    - Option management
- [X] Attribute Controller
    - Attribute management
- [X] Bundle Controller
    - Bundle management
- [X] Review Controller
    - Review management
- [X] Inventory Controller
    - Inventory management
- [X] Price Controller
    - Price management

### Orders
- [X] Order Controller
    - Order processing
    - Status updates
- [X] Fulfillment Controller
    - Shipping management
    - Tracking updates
- [X] OrderNote Controller
    - Note management
- [X] OrderHistory Controller
    - History tracking
- [X] Payment Controller
    - Payment processing
- [X] Refund Controller
    - Refund handling
- [X] Tax Controller
    - Tax calculation

### Cart
- [X] Cart Controller
    - Cart management
    - Item updates
- [X] CartItem Controller
    - Item management
    - Price calculations

### Customers
- [X] Customer Controller
    - Profile management
    - Address management
- [X] CustomerGroup Controller
    - Group management
    - Member assignments

### Payments
- [X] Payment Controller
    - Payment processing
    - Refund handling
- [X] PaymentMethod Controller
    - Method management
    - Gateway configuration

### Shipping
- [X] ShippingZone Controller
    - Zone management
    - Rate calculations
- [X] ShippingMethod Controller
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
- [X] TaxZone Controller
    - Zone management
    - Rate assignments
- [X] TaxCalculation Controller
    - Tax calculations
    - Exemption handling

## Schemas (using Pydantic)

### Core
- [X] UserSchema
- [X] AddressSchema
- [X] ConfigurationSchema

### Products
- [X] ProductSchema
- [X] ProductVariantSchema
- [X] ProductOptionSchema
- [X] CategorySchema
- [X] CollectionSchema
- [X] TagSchema
- [X] AttributeSchema
- [X] BundleSchema
- [X] ReviewSchema

### Orders
- [X] OrderSchema
- [X] OrderLineItemSchema
- [X] FulfillmentSchema
- [X] OrderNoteSchema
- [X] OrderHistorySchema

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
- [X] TaxZoneSchema
- [X] TaxRateSchema
- [X] TaxExemptionSchema

## Additional Tasks

### Documentation
- [X] API Documentation using OpenAPI/Swagger
- [X] Model Documentation
- [X] Setup Instructions
- [X] Deployment Guide

### Testing
- [X] Unit Tests for Models
- [X] Integration Tests for Controllers
- [X] API Tests
- [ ] Performance Tests

### Development Tools
- [X] Data Seeding Scripts
- [X] Development Environment Setup
- [X] Docker Configuration
- [ ] CI/CD Pipeline

### Security
- [X] API Authentication
- [X] Rate Limiting
- [X] Input Validation
- [X] Data Encryption
- [ ] PCI Compliance (for payments)

### Monitoring
- [X] Error Logging
- [X] Performance Monitoring
- [X] Audit Logging
- [ ] Analytics Integration

## Advanced Features
- [X] Multi-currency support
- [X] Multi-language support
- [X] Inventory management with low stock alerts
- [X] Product bundling and kitting
- [X] Dynamic pricing rules
- [X] Customer segmentation
- [X] Abandoned cart recovery
- [X] Order tracking and notifications
- [X] Product reviews and ratings
- [X] SEO optimization for products
- [ ] Recommendation engine
- [ ] A/B testing framework
- [ ] Subscription management
- [ ] Loyalty program
- [ ] Gift cards and store credit
- [ ] Marketplace support (multiple vendors)
- [ ] Dropshipping integration
- [ ] Headless commerce API
- [ ] Omnichannel inventory management
- [ ] Advanced analytics and reporting
