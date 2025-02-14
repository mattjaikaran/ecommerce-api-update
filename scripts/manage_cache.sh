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
    echo "Usage: ./manage_cache.sh [command] [options]"
    echo
    echo "Commands:"
    echo "  clear         Clear all cache"
    echo "  clear-pattern Clear cache matching pattern"
    echo "  stats         Show cache statistics"
    echo "  monitor       Monitor cache usage"
    echo
    echo "Options:"
    echo "  -h, --help    Show this help message"
    echo "  -p PATTERN    Pattern for clear-pattern command"
    echo
    echo "Example:"
    echo "  ./manage_cache.sh clear"
    echo "  ./manage_cache.sh clear-pattern -p 'products:*'"
    echo "  ./manage_cache.sh stats"
}

# Parse command line arguments
COMMAND=""
PATTERN=""

while [[ $# -gt 0 ]]; do
    case $1 in
        clear|stats|monitor|clear-pattern)
            COMMAND=$1
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        -p)
            PATTERN=$2
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

if [ -z "$COMMAND" ]; then
    echo "Error: No command specified"
    show_help
    exit 1
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

# Execute command
case $COMMAND in
    clear)
        echo -e "${BOLD}Clearing all cache...${NC}"
        run_django_cmd "shell -c 'from django.core.cache import cache; cache.clear()'"
        echo -e "${GREEN}Cache cleared successfully${NC}"
        ;;
    clear-pattern)
        if [ -z "$PATTERN" ]; then
            echo -e "${RED}Error: Pattern required for clear-pattern command${NC}"
            exit 1
        fi
        echo -e "${BOLD}Clearing cache matching pattern: $PATTERN${NC}"
        run_django_cmd "shell -c 'from core.cache.settings import clear_cache_pattern; clear_cache_pattern(\"$PATTERN\")'"
        echo -e "${GREEN}Cache pattern cleared successfully${NC}"
        ;;
    stats)
        echo -e "${BOLD}Cache Statistics${NC}"
        run_django_cmd "shell -c 'from django.core.cache import cache; print(cache.info())'"
        ;;
    monitor)
        echo -e "${BOLD}Monitoring cache usage...${NC}"
        echo -e "${YELLOW}Press Ctrl+C to stop${NC}"
        while true; do
            run_django_cmd "shell -c 'from django.core.cache import cache; print(cache.info())'"
            sleep 5
            clear
        done
        ;;
    *)
        echo -e "${RED}Unknown command: $COMMAND${NC}"
        show_help
        exit 1
        ;;
esac
