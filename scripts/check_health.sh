#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Default values
API_URL="http://localhost:8000"
VERBOSE=false
CHECK_DEPS=true
CHECK_DB=true
CHECK_MIGRATIONS=true

# Help message
show_help() {
    echo "Usage: ./check_health.sh [options]"
    echo
    echo "Options:"
    echo "  -h, --help           Show this help message"
    echo "  -v, --verbose        Show detailed output"
    echo "  -u, --url URL        Specify API URL (default: http://localhost:8000)"
    echo "  --skip-deps          Skip dependency checks"
    echo "  --skip-db           Skip database checks"
    echo "  --skip-migrations   Skip migration checks"
    echo
    echo "Example:"
    echo "  ./check_health.sh -v"
    echo "  ./check_health.sh --url http://localhost:8001"
}

# Parse command line arguments
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
        -u|--url)
            API_URL="$2"
            shift 2
            ;;
        --skip-deps)
            CHECK_DEPS=false
            shift
            ;;
        --skip-db)
            CHECK_DB=false
            shift
            ;;
        --skip-migrations)
            CHECK_MIGRATIONS=false
            shift
            ;;
        *)
            echo "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# Function to print status
print_status() {
    local status=$1
    local message=$2
    if [ $status -eq 0 ]; then
        echo -e "${GREEN}✓${NC} $message"
    else
        echo -e "${RED}✗${NC} $message"
        if [ "$VERBOSE" = true ]; then
            echo -e "${RED}  Error: $3${NC}"
        fi
    fi
}

# Check Python dependencies
check_dependencies() {
    echo -e "\n${BOLD}Checking Python dependencies...${NC}"
    
    # Check if pip is installed
    if ! command -v pip &> /dev/null; then
        print_status 1 "pip is not installed" "Please install pip first"
        return 1
    fi
    print_status 0 "pip is installed"

    # Check if requirements.txt exists
    if [ ! -f "requirements.txt" ]; then
        print_status 1 "requirements.txt not found" "Please ensure requirements.txt exists"
        return 1
    fi
    print_status 0 "requirements.txt found"

    # Check installed packages
    echo -e "\n${BLUE}Checking installed packages...${NC}"
    while IFS= read -r requirement; do
        if [[ ! -z "$requirement" && ! "$requirement" =~ ^# ]]; then
            package=$(echo "$requirement" | cut -d'=' -f1)
            if pip freeze | grep -i "^$package=" &> /dev/null; then
                print_status 0 "$package is installed"
            else
                print_status 1 "$package is not installed" "Run: pip install -r requirements.txt"
            fi
        fi
    done < requirements.txt
}

# Check database connection
check_database() {
    echo -e "\n${BOLD}Checking database connection...${NC}"
    
    # Try to run a simple Django command that requires database access
    if python manage.py dbshell --command="SELECT 1;" &> /dev/null; then
        print_status 0 "Database connection successful"
    else
        print_status 1 "Database connection failed" "Check your database settings"
        return 1
    fi
}

# Check migrations
check_migrations() {
    echo -e "\n${BOLD}Checking migrations...${NC}"
    
    # Check for unapplied migrations
    local migrations_output=$(python manage.py showmigrations --plan)
    if echo "$migrations_output" | grep -q "\[ \]"; then
        print_status 1 "Unapplied migrations found" "Run: python manage.py migrate"
        if [ "$VERBOSE" = true ]; then
            echo -e "${YELLOW}Unapplied migrations:${NC}"
            echo "$migrations_output" | grep "\[ \]"
        fi
        return 1
    else
        print_status 0 "All migrations are applied"
    fi
}

# Check API endpoints
check_api() {
    echo -e "\n${BOLD}Checking API endpoints...${NC}"
    
    # Function to check endpoint
    check_endpoint() {
        local endpoint=$1
        local description=$2
        local response=$(curl -s -o /dev/null -w "%{http_code}" "$API_URL$endpoint")
        
        if [ "$response" = "200" ]; then
            print_status 0 "$description ($endpoint)"
        else
            print_status 1 "$description ($endpoint)" "HTTP Status: $response"
            return 1
        fi
    }

    # Check main endpoints
    check_endpoint "/api/products" "Products endpoint"
    check_endpoint "/api/users" "Users endpoint"
    check_endpoint "/api/orders" "Orders endpoint"
    check_endpoint "/api/cart" "Cart endpoint"
}

# Run checks
echo -e "${BOLD}Starting health checks...${NC}"
echo "API URL: $API_URL"

FAILED=0

if [ "$CHECK_DEPS" = true ]; then
    check_dependencies || FAILED=$((FAILED + 1))
fi

if [ "$CHECK_DB" = true ]; then
    check_database || FAILED=$((FAILED + 1))
fi

if [ "$CHECK_MIGRATIONS" = true ]; then
    check_migrations || FAILED=$((FAILED + 1))
fi

check_api || FAILED=$((FAILED + 1))

# Print summary
echo -e "\n${BOLD}Health Check Summary${NC}"
if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}All checks passed!${NC}"
    exit 0
else
    echo -e "${RED}$FAILED check(s) failed${NC}"
    exit 1
fi 