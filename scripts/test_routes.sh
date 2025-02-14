#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color
BOLD='\033[1m'

BASE_URL="http://localhost:8000/api"
AUTH_TOKEN=""
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# Function to print section header
print_header() {
    echo -e "\n${BLUE}${BOLD}=== $1 ===${NC}\n"
}

# Function to print test result
print_result() {
    local name=$1
    local status_code=$2
    local expected_code=$3
    local response=$4
    local time=$5

    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    
    if [ "$status_code" -eq "$expected_code" ]; then
        echo -e "${GREEN}✓ $name${NC} (${time}s)"
        echo -e "  Status: $status_code"
        PASSED_TESTS=$((PASSED_TESTS + 1))
    else
        echo -e "${RED}✗ $name${NC} (${time}s)"
        echo -e "  Expected: $expected_code, Got: $status_code"
        echo -e "  Response: $response"
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
}

# Function to make a request and check response
test_endpoint() {
    local method=$1
    local endpoint=$2
    local description=$3
    local expected_code=$4
    local data=$5

    echo -e "\n${YELLOW}Testing: $description${NC}"
    echo "$method $endpoint"

    start_time=$(date +%s.%N)

    if [ "$method" = "GET" ]; then
        if [ -n "$AUTH_TOKEN" ]; then
            response=$(curl -s -w "\n%{http_code}" -X $method \
                -H "Authorization: Bearer $AUTH_TOKEN" \
                $BASE_URL$endpoint | grep -v "<!DOCTYPE" | grep -v "<html" | grep -v "<head" | grep -v "<body" | grep -v "<script" | grep -v "<style")
        else
            response=$(curl -s -w "\n%{http_code}" -X $method $BASE_URL$endpoint | grep -v "<!DOCTYPE" | grep -v "<html" | grep -v "<head" | grep -v "<body" | grep -v "<script" | grep -v "<style")
        fi
    else
        if [ -n "$data" ]; then
            if [ -n "$AUTH_TOKEN" ]; then
                response=$(curl -s -w "\n%{http_code}" -X $method \
                    -H "Content-Type: application/json" \
                    -H "Authorization: Bearer $AUTH_TOKEN" \
                    -d "$data" \
                    $BASE_URL$endpoint | grep -v "<!DOCTYPE" | grep -v "<html" | grep -v "<head" | grep -v "<body" | grep -v "<script" | grep -v "<style")
            else
                response=$(curl -s -w "\n%{http_code}" -X $method \
                    -H "Content-Type: application/json" \
                    -d "$data" \
                    $BASE_URL$endpoint | grep -v "<!DOCTYPE" | grep -v "<html" | grep -v "<head" | grep -v "<body" | grep -v "<script" | grep -v "<style")
            fi
        else
            if [ -n "$AUTH_TOKEN" ]; then
                response=$(curl -s -w "\n%{http_code}" -X $method \
                    -H "Authorization: Bearer $AUTH_TOKEN" \
                    $BASE_URL$endpoint | grep -v "<!DOCTYPE" | grep -v "<html" | grep -v "<head" | grep -v "<body" | grep -v "<script" | grep -v "<style")
            else
                response=$(curl -s -w "\n%{http_code}" -X $method $BASE_URL$endpoint | grep -v "<!DOCTYPE" | grep -v "<html" | grep -v "<head" | grep -v "<body" | grep -v "<script" | grep -v "<style")
            fi
        fi
    fi

    end_time=$(date +%s.%N)
    execution_time=$(echo "$end_time - $start_time" | bc)
    execution_time=$(printf "%.2f" $execution_time)

    status_code=$(echo "$response" | tail -n1)
    full_body=$(echo "$response" | sed '$d' | grep -v "^[[:space:]]*$")
    
    # Create a truncated version for display
    body="$full_body"
    # Only truncate successful responses with arrays
    if [ "$status_code" -eq 200 ] || [ "$status_code" -eq 201 ]; then
        # Try to parse as JSON and get counts if it's an array
        if echo "$body" | jq -e . >/dev/null 2>&1; then
            # Check if response is an array
            if echo "$body" | jq -e 'if type=="array" then true else false end' >/dev/null 2>&1; then
                count=$(echo "$body" | jq '. | length')
                body="Array response with $count items"
            # Check if response has items array    
            elif echo "$body" | jq -e '.items' >/dev/null 2>&1; then
                count=$(echo "$body" | jq '.items | length')
                body="Response with $count items"
            fi
        fi
    fi

    if [ "$status_code" -eq "$expected_code" ]; then
        echo -e "${GREEN}✓ $description${NC} (${execution_time}s)"
        echo -e "  Status: $status_code"
        if [ -n "$body" ]; then
            echo -e "  Response: $body"
        fi
        PASSED_TESTS=$((PASSED_TESTS + 1))
    else
        echo -e "${RED}✗ $description${NC} (${execution_time}s)"
        echo -e "  Expected: $expected_code, Got: $status_code"
        if [ -n "$body" ]; then
            echo -e "  Response: $body"
        fi
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi

    TOTAL_TESTS=$((TOTAL_TESTS + 1))

    # Store token if this is a login request
    if [ "$endpoint" = "/users/login" ] && [ "$status_code" -eq 200 ]; then
        # Try to extract token from response body
        if echo "$full_body" | jq -e . >/dev/null 2>&1; then
            AUTH_TOKEN=$(echo "$full_body" | jq -r '.token // .access // empty')
            if [ -n "$AUTH_TOKEN" ] && [ "$AUTH_TOKEN" != "null" ]; then
                echo -e "${GREEN}Authentication token obtained${NC}"
            else
                echo -e "${RED}Failed to obtain authentication token${NC}"
                exit 1
            fi
        else
            echo -e "${RED}Invalid JSON response from login${NC}"
            exit 1
        fi
    fi

    # Store IDs for subsequent requests if needed
    if [ "$endpoint" = "/products/" ] && [ "$status_code" -eq 200 ]; then
        PRODUCT_ID=$(echo "$full_body" | jq -r '.items[0].id')
    elif [ "$endpoint" = "/customers/" ] && [ "$status_code" -eq 200 ]; then
        CUSTOMER_ID=$(echo "$full_body" | jq -r '.items[0].id')
    fi
}

echo "=== Starting API Route Testing ==="
echo
echo "Base URL: $BASE_URL"
echo

# Generate a unique username using timestamp
USERNAME="testuser_$(date +%s)"
USER_ID=""

echo "=== Creating Test User ==="
test_endpoint "POST" "/users/signup" "Create Test User" 201 "{\"username\": \"$USERNAME\", \"email\": \"$USERNAME@example.com\", \"password\": \"testpass123\", \"first_name\": \"Test\", \"last_name\": \"User\"}"

# Store the user ID from the response
if [ "$status_code" -eq 201 ]; then
    USER_ID=$(echo "$full_body" | jq -r '.id')
fi

echo

echo "=== Authentication Tests ==="
echo

# Test regular login
test_endpoint "POST" "/users/login" "Regular Login" 200 "{\"username\": \"$USERNAME\", \"password\": \"testpass123\"}"

if [ -z "$AUTH_TOKEN" ]; then
    echo -e "${RED}Authentication failed. Cannot proceed with tests.${NC}"
    exit 1
fi

# User Tests
print_header "User Tests"
test_endpoint "GET" "/users" "List Users" 200
# test_endpoint "GET" "/users/me" "Get Current User" 200

# Customer Tests
print_header "Customer Tests"
test_endpoint "GET" "/customers" "List Customers" 200
if [ -n "$CUSTOMER_ID" ]; then
    test_endpoint "GET" "/customers/$CUSTOMER_ID" "Get Customer by ID" 200
fi

# Product Tests
print_header "Product Tests"
test_endpoint "GET" "/products" "List Products" 200
if [ -n "$PRODUCT_ID" ]; then
    test_endpoint "GET" "/products/$PRODUCT_ID" "Get Product by ID" 200
fi

# Category Tests
print_header "Category Tests"
test_endpoint "GET" "/products/categories" "List Categories" 200

# Collection Tests
print_header "Collection Tests"
test_endpoint "GET" "/products/collections" "List Collections" 200

# Tag Tests
print_header "Tag Tests"
test_endpoint "GET" "/products/tags" "List Tags" 200

# Cart Tests
print_header "Cart Tests"
test_endpoint "GET" "/cart" "Get Cart" 200
if [ -n "$AUTH_TOKEN" ] && [ -n "$PRODUCT_ID" ]; then
    test_endpoint "POST" "/cart/items" "Add Item to Cart" 201 "{\"product_variant_id\": \"$PRODUCT_ID\", \"quantity\": 1}"
fi

# Order Tests
print_header "Order Tests"
test_endpoint "GET" "/orders" "List Orders" 200

# Print summary
print_header "Test Summary"
echo -e "${BOLD}Total Tests: $TOTAL_TESTS${NC}"
echo -e "${GREEN}Passed: $PASSED_TESTS${NC}"
echo -e "${RED}Failed: $FAILED_TESTS${NC}"

# Calculate success rate
success_rate=$(echo "scale=2; ($PASSED_TESTS * 100) / $TOTAL_TESTS" | bc)
echo -e "${BOLD}Success Rate: ${success_rate}%${NC}"

# Clean up - Delete test user if we have their ID
if [ -n "$USER_ID" ] && [ -n "$AUTH_TOKEN" ]; then
    echo -e "\n=== Cleaning Up ==="
    test_endpoint "DELETE" "/users/$USER_ID" "Delete Test User" 204
fi

if [ $FAILED_TESTS -eq 0 ]; then
    echo -e "\n${GREEN}${BOLD}All tests passed successfully!${NC}"
    exit 0
else
    echo -e "\n${RED}${BOLD}Some tests failed. Please check the logs above.${NC}"
    exit 1
fi 