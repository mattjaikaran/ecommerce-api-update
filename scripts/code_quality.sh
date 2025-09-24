#!/bin/bash

# Code quality check script for Django Ecommerce API
# Runs comprehensive code quality checks including linting, formatting, and testing

set -e

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

# Track overall success
OVERALL_SUCCESS=true

# Function to run a check and track result
run_check() {
    local name="$1"
    local command="$2"
    
    print_info "Running $name..."
    
    if eval "$command"; then
        print_success "$name passed!"
        return 0
    else
        print_error "$name failed!"
        OVERALL_SUCCESS=false
        return 1
    fi
}

# Main checks
main() {
    print_info "Starting comprehensive code quality checks..."
    echo ""
    
    # 1. Code formatting check
    run_check "Code formatting check" "uv run ruff format --check ."
    
    # 2. Linting check
    run_check "Linting check" "uv run ruff check ."
    
    # 3. Type checking (if mypy is available)
    if command -v mypy >/dev/null 2>&1; then
        run_check "Type checking" "uv run mypy ."
    else
        print_warning "MyPy not available, skipping type checking"
    fi
    
    # 4. Security check (if bandit is available)
    if command -v bandit >/dev/null 2>&1; then
        run_check "Security check" "uv run bandit -r . -f json"
    else
        print_warning "Bandit not available, skipping security check"
    fi
    
    # 5. Import sorting check
    run_check "Import sorting check" "uv run ruff check --select I ."
    
    # 6. Test suite
    run_check "Test suite" "uv run python -m pytest --tb=short"
    
    # 7. Test coverage
    run_check "Test coverage" "uv run python -m pytest --cov=. --cov-report=term-missing --cov-fail-under=80"
    
    echo ""
    
    if [ "$OVERALL_SUCCESS" = true ]; then
        print_success "All code quality checks passed! ✅"
        exit 0
    else
        print_error "Some code quality checks failed! ❌"
        echo ""
        echo "To fix issues automatically, run:"
        echo "  make fix           # Fix formatting and auto-fixable linting issues"
        echo "  make lint-fix      # Fix linting issues only"
        echo "  make format        # Format code only"
        exit 1
    fi
}

main "$@"
