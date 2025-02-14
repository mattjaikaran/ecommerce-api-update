#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Help message
show_help() {
    echo "Usage: ./reset_test_data.sh [options]"
    echo
    echo "Options:"
    echo "  -h, --help            Show this help message"
    echo "  -f, --force           Skip confirmation prompt"
    echo "  -a, --app APP_NAME    Reset data for specific app only"
    echo "  --no-migrations       Skip running migrations"
    echo
    echo "Available apps:"
    echo "  products    Reset and seed product-related data"
    echo "  orders      Reset and seed order-related data"
    echo "  cart        Reset and seed cart-related data"
    echo "  users       Reset and seed user-related data"
    echo "  all         Reset and seed all data (default)"
    echo
    echo "Example:"
    echo "  ./reset_test_data.sh -f products"
    echo "  ./reset_test_data.sh --app orders"
}

# Parse command line arguments
FORCE=false
APP_NAME="all"
RUN_MIGRATIONS=true

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -f|--force)
            FORCE=true
            shift
            ;;
        -a|--app)
            APP_NAME="$2"
            shift 2
            ;;
        --no-migrations)
            RUN_MIGRATIONS=false
            shift
            ;;
        *)
            echo "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# Confirmation unless force flag is set
if [ "$FORCE" = false ]; then
    echo -e "${YELLOW}Warning: This will delete all existing data for the specified app(s)${NC}"
    read -p "Are you sure you want to continue? [y/N] " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Operation cancelled"
        exit 1
    fi
fi

# Function to run Django management commands
run_django_cmd() {
    echo -e "\n${BLUE}Running: python manage.py $1${NC}"
    python manage.py $1
    if [ $? -ne 0 ]; then
        echo -e "${RED}Failed to run: $1${NC}"
        exit 1
    fi
}

# Reset migrations if requested
if [ "$RUN_MIGRATIONS" = true ]; then
    echo -e "\n${BOLD}Running migrations...${NC}"
    run_django_cmd "migrate"
fi

# Function to reset and seed specific app
reset_app() {
    local app=$1
    echo -e "\n${BOLD}Resetting $app data...${NC}"
    
    case $app in
        products)
            run_django_cmd "generate_product_data"
            ;;
        orders)
            run_django_cmd "generate_order_data"
            ;;
        cart)
            run_django_cmd "generate_cart_data"
            ;;
        users)
            run_django_cmd "generate_user_data"
            ;;
        *)
            echo -e "${RED}Unknown app: $app${NC}"
            exit 1
            ;;
    esac
}

# Reset data based on app name
case $APP_NAME in
    all)
        echo -e "\n${BOLD}Resetting all data...${NC}"
        reset_app "users"
        reset_app "products"
        reset_app "orders"
        reset_app "cart"
        ;;
    products|orders|cart|users)
        reset_app $APP_NAME
        ;;
    *)
        echo -e "${RED}Unknown app: $APP_NAME${NC}"
        show_help
        exit 1
        ;;
esac

echo -e "\n${GREEN}Data reset complete!${NC}" 