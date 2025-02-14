#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Make all scripts executable
echo -e "${BOLD}Making scripts executable...${NC}"
chmod +x scripts/*.sh

# List of core scripts
CORE_SCRIPTS=(
    "test_routes.sh"
    "test_feature.sh"
    "reset_test_data.sh"
    "check_health.sh"
    "db_setup.sh"
    "setup.sh"
    "lint.sh"
    "generate_secret_key.sh"
)

# Verify core scripts
echo -e "\n${BOLD}Verifying core scripts...${NC}"
for script in "${CORE_SCRIPTS[@]}"; do
    if [ -f "scripts/$script" ]; then
        echo -e "${GREEN}✓${NC} $script found"
        if [ -x "scripts/$script" ]; then
            echo -e "  ${GREEN}✓${NC} $script is executable"
        else
            echo -e "  ${RED}✗${NC} $script is not executable"
            chmod +x "scripts/$script"
            echo -e "  ${GREEN}✓${NC} Made $script executable"
        fi
    else
        echo -e "${RED}✗${NC} $script not found"
    fi
done

# Create scripts directory if it doesn't exist
if [ ! -d "scripts" ]; then
    echo -e "\n${YELLOW}Creating scripts directory...${NC}"
    mkdir scripts
fi

# Update README with script documentation
echo -e "\n${BOLD}Updating script documentation...${NC}"
cat > scripts/README.md << 'EOL'
# Development Scripts

This directory contains various scripts to help with development, testing, and maintenance of the API.

## Available Scripts

### Core Scripts
- `test_routes.sh`: Test all API routes
- `test_feature.sh`: Test specific features or endpoints
- `reset_test_data.sh`: Reset and seed test data
- `check_health.sh`: Check API health and dependencies
- `db_setup.sh`: Set up database and run migrations
- `setup.sh`: Initial project setup
- `lint.sh`: Run linting checks
- `generate_secret_key.sh`: Generate Django secret key

### Usage Examples

#### Testing Specific Features
```bash
# Test all product-related endpoints
./test_feature.sh products

# Test with verbose output
./test_feature.sh -v cart
```

#### Resetting Test Data
```bash
# Reset all test data
./reset_test_data.sh

# Reset only product data
./reset_test_data.sh -a products

# Force reset without confirmation
./reset_test_data.sh -f
```

#### Health Checks
```bash
# Run all health checks
./check_health.sh

# Run with verbose output
./check_health.sh -v

# Check specific API URL
./check_health.sh -u http://localhost:8001
```

## Development Guidelines

1. All new scripts should:
   - Be executable
   - Include help documentation
   - Handle errors gracefully
   - Use consistent color coding
   - Include verbose output option

2. Color Coding:
   - Green: Success
   - Red: Error/Failure
   - Yellow: Warning/Caution
   - Blue: Information
   - Bold: Headers/Important information

3. Script Template:
```bash
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
    echo "Usage: ./script_name.sh [options]"
    echo
    echo "Options:"
    echo "  -h, --help     Show this help message"
    # Add other options
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        # Add other options
    esac
done

# Script logic here
```
EOL

echo -e "\n${GREEN}Script setup complete!${NC}"
echo -e "Run ${YELLOW}cat scripts/README.md${NC} to view script documentation" 