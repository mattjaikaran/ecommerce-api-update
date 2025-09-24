# Ecommerce API

E-Commerce API built with Django Ninja and Postgres

## Technologies

- Python 3.12
- [uv](https://docs.astral.sh/uv/) - Fast Python package installer and resolver
- [Django 5.2](https://docs.djangoproject.com/en/5.2/)
- [Django Ninja](https://django-ninja.dev/)
- [Django Ninja Extra](https://eadwincode.github.io/django-ninja-extra/) a collection of extra features for Django Ninja
- [Django Ninja JWT](https://eadwincode.github.io/django-ninja-jwt/)
  - [Django Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/) abstraction for Django Ninja
- [PostgreSQL 17](https://www.postgresql.org/docs/) database
- [Redis 7.2](https://redis.io/) for caching and Celery
- [Pydantic](https://docs.pydantic.dev/latest/)
- [Django Unfold Admin](https://unfoldadmin.com/)
  - [Unfold Docs](https://github.com/unfoldadmin/django-unfold)
- Docker & Docker Compose (optimized for OrbStack)
- [Celery](https://docs.celeryq.dev/) for background tasks
- [Flower](https://flower.readthedocs.io/) for Celery monitoring
- pytest for testing
- Gunicorn for production serving

#### Dev Tools & Features

- **uv** for fast dependency management and virtual environments
- **Ruff** for super-fast linting and formatting (configured in `pyproject.toml`)
- **Makefile** to run commands
- **PyTest** for unit tests with coverage reporting
- **Custom Start App** command to create a new app
  - with extended functionality for Django Ninja, Django Ninja Extra, and Django Unfold
  - `make startapp <app_name>`
- **[Faker](https://faker.readthedocs.io/en/master/)** for generating realistic test data
  - See `@/core/management/commands/generate_core_data.py` for more information
- **[Swagger UI](https://swagger.io/)** for interactive API documentation
  - [Localhost Docs](http://localhost:8000/api/docs)
- **[Debug Toolbar](https://django-debug-toolbar.readthedocs.io/en/latest)** for debugging
- **Environment Variables** for configuration (see `env.example`)
- **Advanced Decorators** for clean controller code:
  - `@handle_exceptions()` - Professional error handling
  - `@log_api_call()` - Request/response logging
  - `@paginate_response()` - Automatic pagination
  - `@search_and_filter()` - Advanced filtering and search
  - `@cached_response()` - Redis caching
  - `@require_authentication()` / `@require_admin()` - Authorization

## 🚀 Quick Start with Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/mattjaikaran/ecommerce-api-update
cd ecommerce-api-update

# Copy environment file
cp env.example .env
# Edit .env with your settings (optional for development)

# Start all services (Django, PostgreSQL, Redis, Celery, Flower)
docker-compose up --build

# In another terminal, run migrations and create superuser
docker-compose exec django python manage.py migrate
docker-compose exec django python manage.py createsuperuser

# Generate test data (optional)
docker-compose exec django python manage.py generate_core_data
```

**🎯 Your services will be available at:**

- **API Documentation**: http://localhost:8000/api/docs
- **Django Admin**: http://localhost:8000/admin
- **Flower (Celery Monitor)**: http://localhost:5555
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379

## 🛠️ Local Development with uv (Alternative)

```bash
# Clone and navigate
git clone https://github.com/mattjaikaran/ecommerce-api-update
cd ecommerce-api-update

# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .

# Set up environment
cp env.example .env
# Edit .env with your local database settings

# Run migrations and create superuser
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Commands

### Start a new Django App

```bash
# start a new django app with extended functionality
# for Django Ninja, Django Ninja Extra, and Django Unfold.
$ make startapp <app_name>
```

### Run Server

```bash
$ make runserver
```

### Install a library

This runs pip install <library-name> , then pip freeze > requirements.txt to update the requirements.txt file

```bash
$ make install <library-name>
# example
# make install django-ninja-jwt
```

### Drop DB, Create DB, Migrate, Create Superuser via db-setup script

```bash
$ make db-setup
```

## Developer Experience Scripts

The project includes several powerful scripts to enhance the development workflow, located in the `scripts/` directory.

### Core Scripts Overview

- `test_feature.sh`: Test specific features or endpoints
- `reset_test_data.sh`: Reset and seed test data
- `check_health.sh`: Check API health and dependencies
- `db_setup.sh`: Set up database and run migrations
- `setup.sh`: Initial project setup
- `lint.sh`: Run linting checks
- `generate_secret_key.sh`: Generate Django secret key

### Testing Features

Test specific parts of the API with detailed output:

```bash
# Test all product-related endpoints
./scripts/test_feature.sh products

# Test cart features with verbose output
./scripts/test_feature.sh -v cart

# Test authentication endpoints
./scripts/test_feature.sh auth

# Test all features
./scripts/test_feature.sh all
```

### Managing Test Data

Reset and seed test data for development:

```bash
# Reset all test data
./scripts/reset_test_data.sh

# Reset only product data
./scripts/reset_test_data.sh -a products

# Force reset without confirmation
./scripts/reset_test_data.sh -f

# Reset data without running migrations
./scripts/reset_test_data.sh --no-migrations
```

### Health Checks

Monitor the health of your API and dependencies:

```bash
# Run all health checks
./scripts/check_health.sh

# Run with verbose output
./scripts/check_health.sh -v

# Check specific API URL
./scripts/check_health.sh -u http://localhost:8001

# Skip specific checks
./scripts/check_health.sh --skip-deps --skip-db
```

### Script Features

All developer scripts include:

- Colored output for better visibility
- Verbose mode for detailed information
- Help documentation (`-h` or `--help`)
- Error handling with descriptive messages
- Consistent formatting and logging

For more detailed documentation about the scripts, see `scripts/README.md`.

### Django Ninja Serialization

- Django Ninja uses Pydantic models (Schemas) for serialization, not Django serializers like in DRF.
- The response parameter in the route decorator specifies the expected response format.
- Use from_orm() to convert Django ORM objects to Pydantic models.
- Django Ninja automatically handles the conversion to JSON in the HTTP response.

## 🏗️ Modern Controller Architecture

All controllers follow a professional, decorator-based pattern with:

- **✅ No Try-Catch Bloat** - Clean code with `@handle_exceptions()` decorator
- **✅ Professional Logging** - Automatic request/response logging with `@log_api_call()` decorator
- **✅ Advanced Filtering** - Built-in search, filtering, and pagination
- **✅ Optimized Queries** - `select_related()` and `prefetch_related()` for performance
- **✅ Consistent Responses** - 201 for creates, 204 for deletes, proper status codes
- **✅ Redis Caching** - Advanced caching with versioning, warming, and management
- **✅ Pagination** - Built-in pagination with `@paginate_response()` decorator
- **✅ Search and Filter** - Built-in search and filtering with `@search_and_filter()` decorator

### Example Controller Pattern:

```python
@api_controller("/products", tags=["Products"])
class ProductController:
    @http_get("", response={200: list[ProductSchema]})
    @list_endpoint(
        cache_timeout=300,
        select_related=["category", "created_by"],
        prefetch_related=["variants", "tags", "images"],
        search_fields=["name", "description", "slug"],
        filter_fields={"category_id": "exact", "status": "exact"},
        ordering_fields=["name", "price", "created_at"],
    )
    @search_and_filter(
        search_fields=["name", "description"],
        filter_fields={"status": "exact"},
    )
    def list_products(self, request):
        return 200, Product.objects.filter(is_active=True)
```

## 🚀 Production Deployment

1. Update `.env` with production settings
2. Build and run with Docker:

```bash
docker-compose -f docker-compose.prod.yml up --build -d
```

## Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest path/to/test_file.py

# Run with coverage
pytest --cov=.
```

## API Documentation

- Swagger UI: `/api/docs`
- ReDoc: `/api/redoc`

## Features

### Core Functionality

- **Complete Ecommerce API** - Products, Cart, Orders, Customers, Payments
- **JWT Authentication** - Django Ninja JWT with refresh tokens
- **Advanced Caching** - Redis with versioning, warming, and management
- **Modern Admin** - Django Unfold admin interface
- **Interactive API Docs** - Swagger/ReDoc with OpenAPI schema

### Database & Storage

- **PostgreSQL 17** - Primary database with optimized schema
- **Redis 7.2** - Caching, sessions, and Celery broker
- **File Storage** - Local development, S3-ready for production

### Development Experience

- **UV Package Management** - Fast Python dependency management
- **Docker Compose** - Development and production configurations
- **Hot Reloading** - Enhanced development server with live reload
- **Enhanced Scripts** - Setup, testing, deployment, and quality checks
- **Comprehensive Testing** - pytest with factories and fixtures

### Code Quality & Monitoring

- **Ruff** - Super-fast linting and formatting
- **Error Handling** - Professional error management with decorators
- **Request Logging** - Comprehensive API call logging
- **Performance Monitoring** - Built-in performance tracking

## Caching System

The project includes a comprehensive Redis-based caching system with the following features:

### Cache Management

1. **Command Line Interface**:

   ```bash
   # Warm cache for specific models
   python manage.py cache_ops warm --models products.Product orders.Order

   # Clear all cache
   python manage.py cache_ops clear --force

   # Preload common queries
   python manage.py cache_ops preload

   # Show cache statistics
   python manage.py cache_ops stats

   # Show cache versions
   python manage.py cache_ops version
   ```

2. **Cache Decorators**:

   ```python
   from core.cache.decorators import cached_view, cached_method

   @api_controller('/products')
   class ProductController:
       @http_get('')
       @cached_view(timeout=300, key_prefix='products')
       def list_products(self):
           return Product.objects.all()

       @cached_method(timeout=300, key_prefix='product')
       def get_product_data(self, product_id):
           return Product.objects.get(id=product_id)
   ```

3. **Versioned Cache**:

   ```python
   from core.cache.versioning import VersionedCache

   # Create versioned cache for a namespace
   cache = VersionedCache('products')

   # Set and get data
   cache.set('featured', featured_products)
   featured = cache.get('featured')

   # Invalidate all cache for namespace
   cache.invalidate_all()
   ```

### Cache Warming

The system includes automatic cache warming for common queries:

1. **Model Cache Warming**:

   ```python
   from core.cache.warming import CacheWarmer

   warmer = CacheWarmer()
   warmer.warm_model(Product, chunk_size=100)
   ```

2. **Query Preloading**:

   ```python
   from core.cache.preload import CachePreloader

   preloader = CachePreloader()
   preloader.preload_products()  # Preload product-related queries
   preloader.preload_all()       # Preload all common queries
   ```

### Admin Interface

The Django admin includes a cache monitoring interface at `/admin/cache-monitor/` with features:

- Cache statistics and metrics
- Cache version management
- Cache warming controls
- Clear cache by namespace
- Monitor cache usage

### Automatic Cache Invalidation

The system automatically invalidates cache when models are updated:

1. **Signal Handlers**:

   ```python
   from core.cache.signals import register_cache_signals

   # In apps.py
   def ready(self):
       register_cache_signals()
   ```

2. **Related Model Invalidation**:
   - When a model is updated, related models' cache is automatically invalidated
   - Handles both forward and reverse relationships

### Configuration

Add to your `settings.py`:

```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'PARSER_CLASS': 'redis.connection.HiredisParser',
            'SOCKET_CONNECT_TIMEOUT': 5,
            'SOCKET_TIMEOUT': 5,
            'COMPRESSOR': 'django_redis.compressors.zlib.ZlibCompressor',
            'IGNORE_EXCEPTIONS': True,
        }
    }
}

# Cache time to live in seconds
CACHE_TTL = 60 * 15  # 15 minutes
CACHE_KEY_PREFIX = 'ecommerce'

# Session backend
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'
```

## 📚 Documentation

Comprehensive documentation is available in the `docs/` directory:

- **[Architecture](docs/architecture.md)** - Detailed system architecture with diagrams and technical specifications
- **[System Design](docs/system-design.md)** - Implementation details, current status, and technology stack
- **[User Journeys](docs/user_journeys.md)** - Customer experience flows and interaction patterns
- **[Machine Learning Features](docs/machine-learning-features.md)** - ML roadmap and learning objectives
- **[Project Tasks](docs/todos.md)** - Implementation status and remaining tasks

### App-Specific Documentation

Each app includes its own README with detailed information:

- **[Core App](core/README.md)** - Authentication, users, customers, and base functionality
- **[Products App](products/README.md)** - Product management, categories, and inventory
- **[Cart App](cart/README.md)** - Shopping cart and session management
- **[Orders App](orders/README.md)** - Order processing, payments, and fulfillment
- **[Scripts](scripts/README.md)** - Development scripts and automation tools

## Database

```bash
$ psql my_db # enter shell
$ createdb --username=USERNAME my_db # create db
$ dropdb my_db # drop db
```
