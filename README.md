# Ecommerce API

E-Commerce API built with Django Ninja and Postgres

## Technologies

- Python 3.11
- [Django 5.2](https://docs.djangoproject.com/en/5.2/)
- [Django Ninja](https://django-ninja.dev/)
- [Django Ninja Extra](https://eadwincode.github.io/django-ninja-extra/) a collection of extra features for Django Ninja
- [Django Ninja JWT](https://eadwincode.github.io/django-ninja-jwt/)
  - [Django Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/) abstraction for Django Ninja
- [Postgres](https://www.postgresql.org/docs/) database
- [Pydantic](https://docs.pydantic.dev/latest/)
- [Django Unfold Admin](https://unfoldadmin.com/)
  - [Unfold Docs](https://github.com/unfoldadmin/django-unfold)
- Docker & Docker Compose
- pytest for testing
- Gunicorn for production serving

#### Dev Tools & Features

- Makefile to run commands
- PyTest for unit tests
- Custom Start App command to create a new app
  - with extended functionality for Django Ninja, Django Ninja Extra, and Django Unfold
  - `make startapp <app_name>`
- [Faker](https://faker.readthedocs.io/en/master/) for generating fake data.
  - See `@/core/management/commands/generate_core_data.py` for more information
- [Swagger](https://swagger.io/) for API documentation
  - [Localhost Docs](http://localhost:8000/api/docs)
- [Debug Toolbar](https://django-debug-toolbar.readthedocs.io/en/latest) for debugging
- [Django Environ](https://django-environ.readthedocs.io/en/latest/) for managing environment variables
- Linting
  - [Ruff](https://github.com/astral-sh/ruff) Formatter
    - Configuration located in `@/.vscode/settings.json`
  - Will run all 3 with the lint script located in `@/scripts/lint.sh`
    - To run `./scripts/lint.sh`

## Quick Start with Docker

```bash
# Clone the repository
git clone https://github.com/mattjaikaran/django-ninja-boilerplate
cd django-ninja-boilerplate

# Create environment file
cp .env.example .env
# Edit .env with your settings

# Start the services
docker-compose up --build
```

Visit http://localhost:8000/api/docs for the API documentation.

## Local Development Setup

```bash
git clone https://github.com/mattjaikaran/django-ninja-boilerplate
cd django-ninja-boilerplate
# Create and activate virtual environment
python3 -m venv env # create a virtual environment using the venv virtual environment
source env/bin/activate # activate the virtual environment
touch .env # create a new env file
# update the .env file with necessary values -> db info, superuser info
pip3 install -r requirements.txt # install dependencies from requirements.txt
python3 manage.py migrate # apply migration files to your local db
python3 manage.py create_superuser # runs custom script to create a superuser
./scripts/generate_secret_key.sh # generate new secret key
python3 manage.py runserver # run the local server on http://localhost:8000/admin
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

## Production Deployment

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

- JWT Authentication
- Passwordless Authentication
- PostgreSQL Database
- Docker & Docker Compose setup
- Comprehensive test setup with pytest
- Code formatting with Ruff
- Production-ready with Gunicorn
- Environment-based settings
- Custom user model
- Admin panel with Django Unfold
- API throttling and pagination
- CORS configuration
- Debug toolbar for development

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

## Database

```bash
$ psql my_db # enter shell
$ createdb --username=USERNAME my_db # create db
$ dropdb my_db # drop db
```
