# 🚀 Enhanced Development Scripts

This directory contains enhanced utility scripts for the Django ecommerce API project with modern tooling and UV package management.

## ⭐ Featured Scripts

### 🛠️ Core Development Scripts

- `dev_setup.sh` - **NEW**: Complete development environment setup with UV
- `code_quality.sh` - **NEW**: Comprehensive code quality checks
- `deploy.sh` - **NEW**: Multi-environment deployment script

### 📊 Legacy Scripts (Still Available)

- `setup.sh` - Basic project setup
- `check_health.sh` - Check application health status
- `reset_test_data.sh` - Reset test database with fresh data
- `db_setup.sh` - Database initialization and setup
- `check_data.sh` - Validate database data integrity
- `manage_cache.sh` - Redis cache management utilities
- `setup_redis.sh` - Redis configuration and setup
- `test_feature.sh` - Run feature-specific tests
- `test_routes.sh` - Test API endpoints
- `generate_secret_key.sh` - Generate Django secret keys
- `lint.sh` - Code linting and formatting
- `setup_scripts.sh` - Make all scripts executable

## 🎯 Quick Start

### Complete Development Setup

```bash
# One-command setup for new developers
./scripts/dev_setup.sh
```

This script will:

- ✅ Check system requirements (Docker, UV, Make)
- ⚙️ Setup environment file from template
- 📦 Install Python dependencies with UV
- 🔧 Configure pre-commit hooks
- 🐳 Build and start Docker services
- 🗃️ Setup database with migrations
- 🔍 Verify installation
- 📊 Display useful URLs and commands

### Code Quality Checks

```bash
# Run all quality checks
./scripts/code_quality.sh
```

Includes:

- 🎨 Code formatting (Ruff)
- 🔍 Linting (Ruff)
- 🏷️ Type checking (MyPy)
- 🔒 Security analysis (Bandit)
- 📥 Import sorting
- 🧪 Test suite with coverage

### Deployment

```bash
# Deploy to staging
./scripts/deploy.sh staging

# Deploy to production (with safety checks)
./scripts/deploy.sh production
```

## 🛠️ Development Workflow

### Daily Development

```bash
# Start development environment
make up

# Run quality checks before committing
./scripts/code_quality.sh

# Fix issues automatically
make fix

# Run specific tests
make test
```

### Environment Management

```bash
# Install new dependency
make add PACKAGE=requests

# Install development dependency
make add-dev PACKAGE=pytest-mock

# Sync dependencies
make sync

# Update lock file
make lock
```

## 📋 Available Make Commands

Run `make help` to see all available commands:

### Package Management (UV)

- `make install` - Install dependencies
- `make sync` - Sync dependencies
- `make add` - Add new dependency
- `make add-dev` - Add dev dependency
- `make lock` - Update lock file

### Development Tools

- `make run-server` - Run Django dev server
- `make run-worker` - Run Celery worker
- `make shell-uv` - Open UV shell
- `make check` - Run all checks
- `make fix` - Fix auto-fixable issues

### Docker Operations

- `make up` - Start services
- `make down` - Stop services
- `make logs` - View logs
- `make shell` - Django shell in container

### Database Operations

- `make migrate` - Run migrations
- `make makemigrations` - Create migrations
- `make flush-db` - Flush database
- `make seed-data` - Load initial data

### Testing & Quality

- `make test` - Run tests
- `make test-coverage` - Run with coverage
- `make lint` - Run linting
- `make format` - Format code
- `make mypy` - Type checking

## 🔧 System Requirements

### Required Tools

- **Docker** (v20.0+) and **Docker Compose** (v2.0+)
- **UV** (latest) - Python package manager
- **Make** - Build automation
- **Git** - Version control

### Optional Tools

- **Pre-commit** - Git hooks for code quality
- **MyPy** - Static type checking
- **Bandit** - Security linting

## 📁 Project Structure Integration

These scripts work with the enhanced project structure:

```
├── api/
│   ├── config/          # Configuration constants
│   │   ├── constants.py
│   │   ├── error_messages.py
│   │   └── settings.py
│   └── utils/           # Utility functions
│       ├── cache.py
│       ├── email.py
│       └── validation.py
├── */models/            # Organized model files
│   ├── __init__.py
│   └── *.py
└── scripts/             # Enhanced development scripts
    ├── dev_setup.sh     # Complete setup
    ├── code_quality.sh  # Quality checks
    └── deploy.sh        # Deployment
```

## 📊 Legacy Script Examples

### Testing Specific Features

```bash
# Test all product-related endpoints
./test_feature.sh products

# Test with verbose output
./test_feature.sh -v cart
```

### Resetting Test Data

```bash
# Reset all test data
./reset_test_data.sh

# Reset only product data
./reset_test_data.sh -a products

# Force reset without confirmation
./reset_test_data.sh -f
```

### Health Checks

```bash
# Run all health checks
./check_health.sh

# Run with verbose output
./check_health.sh -v

# Check specific API URL
./check_health.sh -u http://localhost:8001
```

## 🎯 Best Practices

### Before Committing

1. Run `./scripts/code_quality.sh`
2. Fix any issues with `make fix`
3. Ensure tests pass
4. Verify docs are updated

### Before Deploying

1. Merge to appropriate branch
2. Run full test suite
3. Check environment variables
4. Use deployment script
5. Verify deployment health

### Script Development Guidelines

1. All new scripts should:

   - Be executable (`chmod +x`)
   - Include help documentation
   - Handle errors gracefully
   - Use consistent color coding
   - Include verbose output option

2. Color Coding:

   - 🟢 Green: Success
   - 🔴 Red: Error/Failure
   - 🟡 Yellow: Warning/Caution
   - 🔵 Blue: Information
   - **Bold**: Headers/Important information

3. Script Template:

```bash
#!/bin/bash

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

show_help() {
    echo "Usage: $0 [options]"
    echo
    echo "Options:"
    echo "  -h, --help     Show this help message"
    echo "  -v, --verbose  Enable verbose output"
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        *)
            print_error "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# Main script logic here
main() {
    print_info "Starting script..."
    # Your code here
    print_success "Script completed!"
}

main "$@"
```

## 🆘 Troubleshooting

### Common Issues

**UV not found:**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.cargo/bin:$PATH"
```

**Docker permission issues:**

```bash
sudo usermod -aG docker $USER
# Then log out and back in
```

**Services not starting:**

```bash
make logs  # Check service logs
make down && make up  # Restart all services
```

**Database connection issues:**

```bash
make db-shell  # Test database connection
docker-compose restart db  # Restart database
```

For more help, check the main project README or create an issue.

## 🔗 Related Documentation

- [Main README](../README.md) - Project overview and setup
- [Architecture](../docs/architecture.md) - System architecture
- [API Documentation](http://localhost:8000/api/docs) - Interactive API docs
- [Makefile](../Makefile) - Available make commands
