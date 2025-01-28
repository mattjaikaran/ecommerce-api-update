# TODO

## Apps Structure
- [ ] Core App
    - Authentication, Users, Base Models
    - Permissions and Groups
    - Settings and Configuration
- [ ] Products App
    - Products, Variants, Options
    - Categories and Collections
    - Inventory Management
    - Digital Products Support
- [ ] Orders App
    - Orders and Line Items
    - Order Status Management
    - Order History
    - Fulfillment Tracking
- [ ] Cart App
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

## Models

### Core
- [ ] User Model (Already exists)
    - Extended Django User with e-commerce fields
- [ ] Address Model
    - Support for multiple address types
- [ ] Configuration Model
    - Store settings and preferences

### Products
- [ ] Product Model
    - Base product information
    - SEO fields
    - Status (draft, active, archived)
- [ ] ProductVariant Model
    - SKU, barcode
    - Price, compare at price
    - Inventory tracking
- [ ] ProductOption Model
    - Color, size, material etc
- [ ] ProductImage Model
    - Image management
    - Alt text, position
- [ ] Category Model
    - Hierarchical categories
    - SEO fields
- [ ] Collection Model
    - Curated product groups
    - Automated collections

### Orders
- [ ] Order Model
    - Order details
    - Status management
    - Financial details
- [ ] OrderLineItem Model
    - Product variants
    - Quantities
    - Prices at time of order
- [ ] FulfillmentOrder Model
    - Shipping details
    - Tracking information
- [ ] OrderNote Model
    - Internal and customer notes

### Cart
- [ ] Cart Model
    - Session management
    - Expiry handling
- [ ] CartItem Model
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
- [ ] Authentication Controller
    - JWT token management
    - Permission checking
- [ ] User Controller
    - User management
    - Profile updates

### Products
- [ ] Product Controller
    - CRUD operations
    - Variant management
- [ ] Category Controller
    - Hierarchical management
- [ ] Collection Controller
    - Collection management
    - Product assignments

### Orders
- [ ] Order Controller
    - Order processing
    - Status updates
- [ ] Fulfillment Controller
    - Shipping management
    - Tracking updates

### Cart
- [ ] Cart Controller
    - Cart management
    - Item updates
- [ ] CartCalculation Controller
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
- [ ] UserSchema
- [ ] AddressSchema
- [ ] ConfigurationSchema

### Products
- [ ] ProductSchema
- [ ] ProductVariantSchema
- [ ] ProductOptionSchema
- [ ] CategorySchema
- [ ] CollectionSchema

### Orders
- [ ] OrderSchema
- [ ] OrderLineItemSchema
- [ ] FulfillmentSchema
- [ ] OrderNoteSchema

### Cart
- [ ] CartSchema
- [ ] CartItemSchema
- [ ] CartCalculationSchema

### Customers
- [ ] CustomerSchema
- [ ] CustomerGroupSchema
- [ ] CustomerAddressSchema

### Payments
- [ ] PaymentMethodSchema
- [ ] TransactionSchema
- [ ] RefundSchema

### Shipping
- [ ] ShippingZoneSchema
- [ ] ShippingMethodSchema
- [ ] ShippingRateSchema

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
- [ ] Data Seeding Scripts
- [ ] Development Environment Setup
- [ ] Docker Configuration
- [ ] CI/CD Pipeline

### Security
- [ ] API Authentication
- [ ] Rate Limiting
- [ ] Input Validation
- [ ] Data Encryption
- [ ] PCI Compliance (for payments)

### Monitoring
- [ ] Error Logging
- [ ] Performance Monitoring
- [ ] Audit Logging
- [ ] Analytics Integration
