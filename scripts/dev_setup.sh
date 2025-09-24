#!/bin/bash

# Enhanced development environment setup script for Django Ecommerce API
# This script sets up the complete development environment with UV package management

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
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

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check system requirements
check_requirements() {
    print_info "Checking system requirements..."
    
    # Check for Docker
    if ! command_exists docker; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    # Check for Docker Compose
    if ! command_exists docker-compose; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    # Check for UV
    if ! command_exists uv; then
        print_warning "UV is not installed. Installing UV..."
        curl -LsSf https://astral.sh/uv/install.sh | sh
        export PATH="$HOME/.cargo/bin:$PATH"
        if ! command_exists uv; then
            print_error "Failed to install UV. Please install it manually."
            exit 1
        fi
    fi
    
    # Check for Make
    if ! command_exists make; then
        print_error "Make is not installed. Please install make first."
        exit 1
    fi
    
    print_success "All requirements are satisfied!"
}

# Function to setup environment file
setup_env_file() {
    print_info "Setting up environment file..."
    
    if [ ! -f .env ]; then
        if [ -f env.example ]; then
            cp env.example .env
            print_success "Created .env file from env.example"
            print_warning "Please edit .env file with your configuration before continuing."
            print_info "Key settings to configure:"
            echo "  - Database credentials"
            echo "  - Redis settings"
            echo "  - Email configuration"
            echo "  - Payment gateway keys"
            echo "  - AWS S3 settings (if using)"
            read -p "Press Enter after editing .env file..."
        else
            print_error "env.example file not found. Please create one."
            exit 1
        fi
    else
        print_info ".env file already exists. Skipping creation."
    fi
}

# Function to setup Python environment
setup_python_env() {
    print_info "Setting up Python environment with UV..."
    
    # Install project dependencies
    uv pip install -e .
    
    # Install development dependencies
    uv pip install -e ".[dev]"
    
    print_success "Python environment setup complete!"
}

# Function to setup pre-commit hooks
setup_pre_commit() {
    print_info "Setting up pre-commit hooks..."
    
    if command_exists pre-commit; then
        # Create pre-commit config if it doesn't exist
        if [ ! -f .pre-commit-config.yaml ]; then
            cat > .pre-commit-config.yaml << EOF
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.7.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-merge-conflict
EOF
        fi
        
        uv run pre-commit install
        print_success "Pre-commit hooks installed!"
    else
        print_warning "Pre-commit not available. Install it with: uv add --dev pre-commit"
    fi
}

# Function to build and start services
setup_docker_services() {
    print_info "Building and starting Docker services..."
    
    # Build images
    docker-compose build
    
    # Start services in detached mode
    docker-compose up -d
    
    # Wait for services to be ready
    print_info "Waiting for services to start..."
    sleep 15
    
    # Check if services are running
    if docker-compose ps | grep -q "Up"; then
        print_success "Docker services are running!"
    else
        print_error "Some services failed to start. Check with: docker-compose logs"
        exit 1
    fi
}

# Function to setup database
setup_database() {
    print_info "Setting up database..."
    
    # Run migrations
    docker-compose exec django python manage.py migrate
    
    # Create superuser if in interactive mode
    if [ -t 0 ]; then
        print_info "Creating superuser account..."
        docker-compose exec django python manage.py createsuperuser
    fi
    
    # Load initial data if fixtures exist
    if [ -f fixtures/initial_data.json ]; then
        print_info "Loading initial data..."
        docker-compose exec django python manage.py loaddata fixtures/initial_data.json
    fi
    
    print_success "Database setup complete!"
}

# Function to verify installation
verify_installation() {
    print_info "Verifying installation..."
    
    # Check web server
    if curl -f http://localhost:8000/health/ >/dev/null 2>&1; then
        print_success "Web server is responding!"
    else
        print_warning "Web server is not responding. Check logs with: make logs-django"
    fi
    
    # Check Celery worker
    if curl -f http://localhost:5555/ >/dev/null 2>&1; then
        print_success "Celery Flower is responding!"
    else
        print_warning "Celery Flower is not responding. Check logs with: make logs-celery"
    fi
    
    print_success "Installation verification complete!"
}

# Function to display final information
show_final_info() {
    print_success "Development environment setup complete!"
    echo ""
    echo "Available URLs:"
    echo "  📋 Django Admin: http://localhost:8000/admin"
    echo "  📖 API Documentation: http://localhost:8000/api/docs"
    echo "  🌸 Celery Flower: http://localhost:5555"
    echo "  🏥 Health Check: http://localhost:8000/health"
    echo ""
    echo "Useful commands:"
    echo "  make help              - Show all available commands"
    echo "  make logs              - View all service logs"
    echo "  make shell             - Open Django shell"
    echo "  make test              - Run tests"
    echo "  make lint              - Run code linting"
    echo "  make format            - Format code"
    echo ""
    echo "Happy coding! 🚀"
}

# Main execution
main() {
    print_info "Starting Django Ecommerce API development environment setup..."
    
    check_requirements
    setup_env_file
    setup_python_env
    setup_pre_commit
    setup_docker_services
    setup_database
    verify_installation
    show_final_info
}

# Run main function
main "$@"
