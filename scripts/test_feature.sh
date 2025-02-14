#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color
BOLD='\033[1m'

BASE_URL="http://localhost:8000/api"

# Help message
show_help() {
    echo "Usage: ./test_feature.sh [options] <feature>"
    echo
    echo "Options:"
    echo "  -h, --help     Show this help message"
    echo "  -v, --verbose  Show detailed response output"
    echo
    echo "Available features:"
    echo "  products       Test all product-related endpoints"
    echo "  orders        Test all order-related endpoints"
    echo "  cart          Test all cart-related endpoints"
    echo "  users         Test all user-related endpoints"
    echo "  auth          Test authentication endpoints"
    echo "  all           Test all endpoints"
    echo
    echo "Example:"
    echo "  ./test_feature.sh products"
    echo "  ./test_feature.sh -v cart"
}

# Parse command line arguments
VERBOSE=false
FEATURE=""

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
            FEATURE=$1
            shift
            ;;
    esac
done

if [ -z "$FEATURE" ]; then
    echo "Error: No feature specified"
    show_help
    exit 1
fi

# Source the common test functions
source ./test_routes.sh

# Function to run product tests
test_products() {
    print_header "Testing Product Features"
    test_endpoint "GET" "/products" "List Products" 200
    test_endpoint "GET" "/products/categories" "List Categories" 200
    test_endpoint "GET" "/products/collections" "List Collections" 200
    test_endpoint "GET" "/products/tags" "List Tags" 200
    test_endpoint "GET" "/products/options" "List Product Options" 200
    test_endpoint "GET" "/products/attributes" "List Attributes" 200
    test_endpoint "GET" "/products/bundles" "List Bundles" 200
}

# Function to run order tests
test_orders() {
    print_header "Testing Order Features"
    test_endpoint "GET" "/orders" "List Orders" 200
    test_endpoint "GET" "/orders/fulfillments" "List Fulfillments" 200
}

# Function to run cart tests
test_cart() {
    print_header "Testing Cart Features"
    test_endpoint "GET" "/cart" "Get Cart" 200
    test_endpoint "GET" "/cart/items" "List Cart Items" 200
}

# Function to run user tests
test_users() {
    print_header "Testing User Features"
    test_endpoint "GET" "/users" "List Users" 200
    test_endpoint "GET" "/users/me" "Get Current User" 200
}

# Function to run auth tests
test_auth() {
    print_header "Testing Authentication"
    USERNAME="testuser_$(date +%s)"
    test_endpoint "POST" "/users/signup" "Create Test User" 201 "{\"username\": \"$USERNAME\", \"email\": \"$USERNAME@example.com\", \"password\": \"testpass123\", \"first_name\": \"Test\", \"last_name\": \"User\"}"
    test_endpoint "POST" "/users/login" "Login Test User" 200 "{\"username\": \"$USERNAME\", \"password\": \"testpass123\"}"
}

# Run tests based on feature
case $FEATURE in
    products)
        test_products
        ;;
    orders)
        test_orders
        ;;
    cart)
        test_cart
        ;;
    users)
        test_users
        ;;
    auth)
        test_auth
        ;;
    all)
        test_auth
        test_products
        test_orders
        test_cart
        test_users
        ;;
    *)
        echo "Error: Unknown feature '$FEATURE'"
        show_help
        exit 1
        ;;
esac

# Print summary
echo -e "\n${BOLD}Test Summary${NC}"
echo -e "Total Tests: $TOTAL_TESTS"
echo -e "${GREEN}Passed: $PASSED_TESTS${NC}"
echo -e "${RED}Failed: $FAILED_TESTS${NC}" 