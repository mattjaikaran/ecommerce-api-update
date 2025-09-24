# System Design & Technical Architecture

## Overview

The ecommerce platform is built as a Django application using Django Ninja for API development. It provides APIs for managing products, orders, carts, and user interactions with a focus on developer experience and production deployment.

### Key Features

- **Modern Tooling**: UV package management, Docker containerization
- **Organized Structure**: Modular models and utilities
- **Developer Experience**: Hot reloading, automated scripts, code quality tools
- **API Documentation**: Swagger/OpenAPI integration
- **Containerized Development**: Docker-based development with hot reloading

## Architecture

### Backend Architecture

- Monolithic Django 5.2+ application
- Django Ninja Extra for API development
- PostgreSQL for primary database
- Redis for caching and session management
- Celery for background tasks
- S3 for file storage
- Stripe for payment processing

### Technology Stack

- Django 5.2+ with Django Ninja for API development
- PostgreSQL for database
- Redis for caching and Celery broker
- Celery for background tasks
- Docker for containerization
- UV for fast Python package management

## Core Components

### Project Structure

```
ecommerce-api/
├── api/                    # Core configuration & shared utilities
│   ├── config/            # Centralized configuration
│   │   ├── constants.py   # Application constants
│   │   ├── error_messages.py # Standardized messages
│   │   └── settings.py    # Runtime settings
│   └── utils/             # Utility modules
│       ├── validation.py  # Data validation
│       ├── formatting.py  # Data formatting
│       └── pagination.py  # API pagination
├── core/                  # User management & core models
│   ├── models/            # Core model files
│   ├── controllers/       # API controllers
│   ├── schemas/           # Pydantic schemas
│   └── management/        # Management commands
├── products/              # Product catalog
│   ├── models/            # Product models
│   ├── controllers/       # Product API endpoints
│   └── schemas/           # Product schemas
├── cart/                  # Shopping cart
├── orders/                # Order management
├── payments/              # Payment processing
└── scripts/               # Development scripts
    ├── dev_setup.sh       # Development setup
    ├── code_quality.sh    # Code quality checks
    └── db_setup.sh        # Database setup
```

### API Layer (Django Ninja)

- RESTful API endpoints with OpenAPI documentation
- JWT authentication
- Request validation using Pydantic
- Auto-generated interactive documentation (Swagger/ReDoc)
- CORS support for frontend integration

### Database Design

- PostgreSQL for primary data storage
- Redis for:
  - Session management
  - Cache layer
  - Celery message broker
- Basic database optimization with proper indexing

### Caching Strategy

- Redis-based caching for:
  - Database queries
  - API responses
  - Session storage
- Basic cache invalidation on model updates

### Background Processing

- Celery for async tasks:
  - Order processing
  - Email notifications
  - Report generation
- Basic error handling and retries
- Flower for task monitoring

### File Storage

- Local file storage for development
- S3 integration ready for production
- Basic image handling for product images

### Security

- JWT authentication with Django Ninja JWT
- Input validation using Pydantic
- Django's built-in security features
- CORS configuration
- Environment-based configuration

## Development & Deployment

### Docker Configuration

The application uses Docker for both development and production environments:

#### Development Setup

- **Hot Reloading**: Enabled through volume mounting and custom Django management command
- **Services**:
  - Django web server with hot reloading
  - PostgreSQL 17 database
  - Redis for caching and Celery
  - Celery worker and beat scheduler
  - Flower for Celery monitoring
- **Development Server**: Uses custom `runserver_dev.py` command for enhanced development features

#### Docker Services

```yaml
services:
  django: # Main Django application with hot reloading
  db: # PostgreSQL 17 database
  redis: # Redis for caching and Celery broker
  celery: # Background task worker
  celery-beat: # Task scheduler
  flower: # Celery monitoring interface
```

#### Hot Reloading Setup

The Django service is configured for development with:

1. **Volume Mounting**: Code changes are immediately reflected
2. **Custom Management Command**: `python manage.py runserver_dev` provides:

   - Enhanced hot reloading
   - SQL query printing (with `--print-sql` flag)
   - Automatic admin panel refresh
   - Threading support for better performance

3. **Development Entrypoint**: `docker-entrypoint-dev.sh` handles:
   - UV package management
   - Database and Redis connectivity checks
   - Virtual environment setup

#### Running the Development Environment

```bash
# Start all services with hot reloading
docker-compose up --build

# The Django service runs with hot reloading:
python manage.py runserver_dev 0.0.0.0:8000

# Access points:
# - API Documentation: http://localhost:8000/api/docs
# - Admin Panel: http://localhost:8000/admin
# - Celery Monitoring: http://localhost:5555
```

### Package Management with UV

The project uses UV for fast Python package management:

```bash
# Install dependencies
uv pip install -e .

# Development setup
uv venv .venv
uv pip install --python .venv/bin/python [packages]
```

### Available Scripts

Development scripts in the `scripts/` directory:

- **`dev_setup.sh`**: Development environment setup
- **`code_quality.sh`**: Linting and quality checks
- **`db_setup.sh`**: Database setup and migrations
- **`test_feature.sh`**: Feature testing
- **`check_health.sh`**: API health checks

### Production Deployment

For production, use the production Docker Compose configuration:

```bash
docker-compose -f docker-compose.prod.yml up --build -d
```

## API Documentation

The API provides interactive documentation:

- **Swagger UI**: Available at `/api/docs`
- **ReDoc**: Available at `/api/redoc`
- **OpenAPI Schema**: Auto-generated from Django Ninja

## Testing

The project includes:

- **Unit Tests**: Using pytest
- **Feature Testing**: Custom scripts for endpoint testing
- **Health Checks**: Automated monitoring scripts

## Current Implementation Status

### Implemented Features

- **Core API**: Product, Order, Cart, User management APIs
- **Authentication**: JWT-based authentication system
- **Database**: PostgreSQL with Django ORM
- **Caching**: Redis integration for basic caching
- **Background Tasks**: Celery for async processing
- **Admin Interface**: Django Unfold admin panel
- **Documentation**: Auto-generated API docs
- **Development Tools**: Hot reloading, testing scripts, code quality tools

### Development Focus

- **Code Quality**: Consistent formatting and linting
- **Developer Experience**: Fast setup and hot reloading
- **API Documentation**: Interactive Swagger/ReDoc interfaces
- **Testing**: Unit tests and feature testing scripts
- **Containerization**: Docker-based development and deployment

### Learning Project Roadmap

This is a public learning project designed to demonstrate modern Django development and ML integration. The roadmap includes:

#### Immediate Goals

- Enhanced caching strategies
- Performance optimization
- Additional security features
- Extended API functionality

#### Machine Learning Integration (Learning Phase)

- Product recommendation systems
- Demand forecasting models
- Fraud detection algorithms
- Computer vision for product categorization
- NLP for review analysis

See `machine-learning-features.md` for detailed ML roadmap and learning objectives.

#### Advanced Features (Future Learning)

- Real-time analytics
- A/B testing framework
- Model monitoring and deployment
- MLOps best practices
