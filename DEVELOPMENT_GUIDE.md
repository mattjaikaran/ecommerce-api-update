# 🚀 Development Guide - Modern Django Ecommerce API

## 📋 Overview

This is a modern, scalable Django ecommerce API built with the latest Python tooling and best practices. The project uses **uv** for dependency management, **Ruff** for linting and formatting, and follows a modular architecture for maximum maintainability.

## 🛠 Tech Stack

### Core Technologies

- **Python 3.12** - Latest stable Python version
- **Django 5.1** - High-level Python web framework
- **Django Ninja** - Fast API framework for Django
- **PostgreSQL** - Primary database
- **Redis** - Caching and session storage
- **uv** - Fast Python package installer and resolver
- **Ruff** - Extremely fast Python linter and formatter

### Development Tools

- **VS Code** - Recommended IDE with comprehensive settings
- **Docker** - Containerization for development and deployment
- **pytest** - Testing framework
- **Coverage** - Code coverage reporting

### External Services

- **Stripe** - Payment processing
- **AWS S3** - File storage (optional)
- **SendGrid** - Email delivery (optional)

## 🏗 Project Structure

```
ecommerce-api/
├── api/                    # Main Django project
│   ├── constants.py        # Global constants
│   ├── utils.py           # Common utilities
│   ├── exceptions.py      # Custom exceptions
│   ├── permissions.py     # Authorization logic
│   ├── healthcheck.py     # Health monitoring
│   ├── settings.py        # Django settings
│   └── urls.py            # URL configuration
├── cart/                   # Shopping cart module
├── core/                   # Core functionality (users, auth, etc.)
├── orders/                 # Order management
├── payments/               # Payment processing
├── products/               # Product catalog
├── static/                 # Static files
├── scripts/               # Utility scripts
├── .vscode/               # VS Code configuration
├── pyproject.toml         # Project configuration
├── uv.lock               # Dependency lock file
└── README.md             # Project documentation
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+ installed
- PostgreSQL database
- Redis server (optional, for caching)
- uv package manager

### Installation

1. **Install uv** (if not already installed):

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Clone and setup project**:

   ```bash
   git clone <repository-url>
   cd ecommerce-api-update

   # Install dependencies
   uv sync --dev

   # Activate virtual environment
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Environment Configuration**:

   ```bash
   # Copy environment template
   cp .env.example .env

   # Edit .env with your settings
   nano .env
   ```

4. **Database Setup**:

   ```bash
   # Run migrations
   uv run python manage.py migrate

   # Create superuser
   uv run python manage.py createsuperuser

   # Load sample data (optional)
   uv run python manage.py generate_core_data
   ```

5. **Start Development Server**:
   ```bash
   uv run python manage.py runserver
   ```

## 📝 Development Workflow

### Code Quality

**Linting and Formatting** (using Ruff):

```bash
# Check code quality
make lint
# or
uv run ruff check .

# Format code
make format
# or
uv run ruff format .

# Auto-fix issues
make lint-fix
# or
uv run ruff check --fix .
```

**Testing**:

```bash
# Run all tests
make test
# or
uv run python manage.py test

# Run with pytest
uv run pytest -v

# Run with coverage
uv run pytest --cov=. --cov-report=html
```

### Package Management

**Adding Dependencies**:

```bash
# Add runtime dependency
uv add package-name

# Add development dependency
uv add --dev package-name

# Update all dependencies
uv sync --upgrade
```

**Remove Dependencies**:

```bash
uv remove package-name
```

### Database Management

**Migrations**:

```bash
# Create migrations
uv run python manage.py makemigrations

# Apply migrations
uv run python manage.py migrate

# Reset database (development only)
uv run python manage.py flush
```

## 🔧 VS Code Setup

The project includes comprehensive VS Code configuration:

### Recommended Extensions

- **Python** - Python support
- **Ruff** - Linting and formatting
- **Django** - Django template support
- **Even Better TOML** - pyproject.toml support
- **GitLens** - Enhanced Git integration
- **Docker** - Container support

### Key Features

- **Auto-formatting** on save with Ruff
- **Import sorting** on save
- **Comprehensive debugging** configurations
- **Django-specific** file associations
- **Integrated testing** support

## 🚦 API Endpoints

### Health Checks

- `GET /health/` - Simple health check
- `GET /health/all/` - Comprehensive health check
- `GET /readiness/` - Kubernetes readiness probe
- `GET /liveness/` - Kubernetes liveness probe
- `GET /monitoring/` - Detailed monitoring info

### Core API

- `GET /api/docs` - API documentation
- `POST /api/auth/` - Authentication endpoints
- `GET /api/products/` - Product listings
- `POST /api/cart/` - Cart management
- `GET /api/orders/` - Order management

## 🗄 Database Design

### Core Models

- **User** - Authentication and basic user info
- **Customer** - Extended customer profiles
- **Product** - Product catalog
- **Order** - Order management
- **Cart** - Shopping cart functionality

### Key Features

- **Soft deletes** for audit trails
- **Timestamped models** for tracking
- **UUID primary keys** for security
- **Optimized queries** with select_related/prefetch_related

## 🔐 Authentication & Security

### JWT Authentication

- **Access tokens** for API access
- **Refresh tokens** for token renewal
- **Configurable expiry** times

### Permission System

- **Role-based** access control
- **Object-level** permissions
- **Decorator-based** protection

### Security Features

- **Rate limiting** on sensitive endpoints
- **CORS** configuration
- **Security headers** middleware
- **Input validation** and sanitization

## 📊 Monitoring & Observability

### Health Checks

- **Database** connectivity
- **Redis** availability
- **External service** status
- **System resource** monitoring

### Logging

- **Structured logging** with JSON format
- **Request/response** logging
- **Error tracking** and alerting
- **Performance** monitoring

## 🚀 Deployment

### Docker Deployment

```bash
# Build image
docker build -t ecommerce-api .

# Run with docker-compose
docker-compose up -d
```

### Environment Variables

```env
# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/dbname

# Redis
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com

# External Services
STRIPE_SECRET_KEY=sk_test_...
AWS_ACCESS_KEY_ID=...
```

## 🧪 Testing Strategy

### Test Structure

```
tests/
├── unit/           # Unit tests
├── integration/    # Integration tests
├── fixtures/       # Test data
└── factories/      # Test data factories
```

### Testing Best Practices

- **Factory Boy** for test data generation
- **pytest** fixtures for setup/teardown
- **Mocking** external services
- **Coverage** reporting above 80%

## 📈 Performance Optimization

### Database Optimization

- **Indexes** on frequently queried fields
- **Query optimization** with select_related/prefetch_related
- **Connection pooling** for better performance
- **Read replicas** for scaling reads

### Caching Strategy

- **Redis** for session and cache storage
- **Memcached** for object caching
- **CDN** for static assets
- **Database query** caching

### API Performance

- **Pagination** for large datasets
- **Field selection** to reduce payload size
- **Compression** for responses
- **Rate limiting** to prevent abuse

## 🔄 CI/CD Pipeline

### GitHub Actions Workflow

1. **Code quality** checks (Ruff)
2. **Security** scanning
3. **Test execution** with coverage
4. **Docker image** building
5. **Deployment** to staging/production

### Quality Gates

- **All tests** must pass
- **Code coverage** above 80%
- **No security** vulnerabilities
- **Performance** benchmarks met

## 📚 Additional Resources

### Documentation

- [Django Documentation](https://docs.djangoproject.com/)
- [Django Ninja Documentation](https://django-ninja.rest-framework.com/)
- [uv Documentation](https://docs.astral.sh/uv/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)

### Best Practices

- [Django Best Practices](https://django-best-practices.readthedocs.io/)
- [API Design Guidelines](https://github.com/microsoft/api-guidelines)
- [12-Factor App](https://12factor.net/)

## 🆘 Troubleshooting

### Common Issues

**Database Connection Issues**:

```bash
# Check database status
uv run python manage.py dbshell

# Reset migrations (development only)
uv run python manage.py migrate --fake-initial
```

**Cache Issues**:

```bash
# Clear cache
uv run python manage.py clear_cache

# Test Redis connection
redis-cli ping
```

**Import Errors**:

```bash
# Regenerate lock file
uv lock

# Reinstall dependencies
uv sync --reinstall
```

## 👥 Contributing

1. **Create feature branch** from main
2. **Follow code style** (enforced by Ruff)
3. **Write tests** for new functionality
4. **Update documentation** as needed
5. **Submit pull request** with clear description

### Code Review Checklist

- [ ] Code follows project standards
- [ ] Tests are included and passing
- [ ] Documentation is updated
- [ ] Security considerations addressed
- [ ] Performance impact assessed

---

For more information, see the [API Documentation](http://localhost:8000/api/docs) when running locally.
