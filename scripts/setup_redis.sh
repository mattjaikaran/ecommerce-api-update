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
    echo "Usage: ./setup_redis.sh [options]"
    echo
    echo "Options:"
    echo "  -h, --help            Show this help message"
    echo "  -f, --force           Skip confirmation prompt"
    echo "  --skip-docker         Skip Docker configuration"
    echo
    echo "This script will:"
    echo "  1. Install Redis dependencies"
    echo "  2. Update Docker configuration"
    echo "  3. Configure Django settings"
    echo "  4. Add cache management scripts"
}

# Parse command line arguments
FORCE=false
SETUP_DOCKER=true

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
        --skip-docker)
            SETUP_DOCKER=false
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
    echo -e "${YELLOW}This will modify your project configuration to add Redis support.${NC}"
    read -p "Are you sure you want to continue? [y/N] " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Operation cancelled"
        exit 1
    fi
fi

# Install Redis dependencies
echo -e "\n${BOLD}Installing Redis dependencies...${NC}"
pip install django-redis redis hiredis
pip freeze > requirements.txt
echo -e "${GREEN}✓${NC} Redis dependencies installed"

# Update Docker configuration if needed
if [ "$SETUP_DOCKER" = true ]; then
    echo -e "\n${BOLD}Updating Docker configuration...${NC}"
    
    # Add Redis service to docker-compose.yml
    if [ -f "docker-compose.yml" ]; then
        # Check if Redis service already exists
        if ! grep -q "redis:" docker-compose.yml; then
            cat >> docker-compose.yml << 'EOL'

  redis:
    image: redis:7.2-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes
    networks:
      - app-network

volumes:
  redis_data:
EOL
            echo -e "${GREEN}✓${NC} Added Redis service to docker-compose.yml"
        else
            echo -e "${YELLOW}⚠ Redis service already exists in docker-compose.yml${NC}"
        fi
    else
        echo -e "${RED}✗ docker-compose.yml not found${NC}"
    fi
fi

# Create cache configuration
echo -e "\n${BOLD}Creating cache configuration...${NC}"
mkdir -p core/cache
touch core/cache/__init__.py

# Create cache settings file
cat > core/cache/settings.py << 'EOL'
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.conf import settings

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

def cache_key_prefix(key: str) -> str:
    """Generate a cache key with the appropriate prefix."""
    return f"{settings.CACHE_KEY_PREFIX}:{key}"

def get_cached_data(key: str, default=None):
    """Get data from cache with proper key prefix."""
    return cache.get(cache_key_prefix(key), default)

def set_cached_data(key: str, value, timeout=CACHE_TTL):
    """Set data in cache with proper key prefix."""
    return cache.set(cache_key_prefix(key), value, timeout)

def delete_cached_data(key: str):
    """Delete data from cache with proper key prefix."""
    return cache.delete(cache_key_prefix(key))

def clear_cache_pattern(pattern: str):
    """Clear all cache keys matching a pattern."""
    keys = cache.keys(f"{settings.CACHE_KEY_PREFIX}:{pattern}")
    return cache.delete_many(keys)
EOL

# Create cache decorator file
cat > core/cache/decorators.py << 'EOL'
from functools import wraps
from django.core.cache import cache
from .settings import cache_key_prefix, CACHE_TTL

def cached_view(timeout=CACHE_TTL, key_prefix='view'):
    """
    Cache decorator for API views.
    Usage:
        @cached_view(timeout=300, key_prefix='products')
        def get_products(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Generate cache key based on the full URL path and query parameters
            cache_key = f"{key_prefix}:{request.get_full_path()}"
            response = cache.get(cache_key_prefix(cache_key))
            
            if response is None:
                response = view_func(request, *args, **kwargs)
                cache.set(cache_key_prefix(cache_key), response, timeout)
            
            return response
        return _wrapped_view
    return decorator

def cached_method(timeout=CACHE_TTL, key_prefix='method'):
    """
    Cache decorator for class methods.
    Usage:
        @cached_method(timeout=300, key_prefix='user')
        def get_user_data(self, user_id):
            ...
    """
    def decorator(method):
        @wraps(method)
        def _wrapped_method(self, *args, **kwargs):
            # Generate cache key based on method arguments
            cache_key = f"{key_prefix}:{':'.join(map(str, args))}"
            if kwargs:
                cache_key += f":{':'.join(f'{k}={v}' for k, v in sorted(kwargs.items()))}"
            
            result = cache.get(cache_key_prefix(cache_key))
            
            if result is None:
                result = method(self, *args, **kwargs)
                cache.set(cache_key_prefix(cache_key), result, timeout)
            
            return result
        return _wrapped_method
    return decorator
EOL

# Create cache management script
cat > scripts/manage_cache.sh << 'EOL'
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
EOL

# Make the cache management script executable
chmod +x scripts/manage_cache.sh

# Update Django settings
echo -e "\n${BOLD}Updating Django settings...${NC}"
echo -e "${YELLOW}Please add the following to your settings.py:${NC}"
echo -e """
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'PARSER_CLASS': 'redis.connection.HiredisParser',
            'SOCKET_CONNECT_TIMEOUT': 5,
            'SOCKET_TIMEOUT': 5,
            'COMPRESSOR': 'django_redis.compressors.zlib.ZlibCompressor',
            'IGNORE_EXCEPTIONS': True,
        }
    }
}

# Cache time to live in seconds
CACHE_TTL = 60 * 15  # 15 minutes
CACHE_KEY_PREFIX = 'ecommerce'

# Session backend
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'
"""

echo -e "\n${GREEN}Redis setup complete!${NC}"
echo -e "You can now use the cache management script: ${YELLOW}./scripts/manage_cache.sh${NC}"
echo -e "Don't forget to update your settings.py with the cache configuration!" 