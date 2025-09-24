#!/bin/bash

# Django Development Server with Hot Reloading
# This script starts the Django development server with enhanced hot reloading capabilities

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Starting Django Development Server with Hot Reloading${NC}"
echo -e "${YELLOW}📁 Working directory: $(pwd)${NC}"

# Check if Django is available
if ! python manage.py --version > /dev/null 2>&1; then
    echo -e "${RED}❌ Error: Django not found. Make sure you're in the project directory and Django is installed.${NC}"
    exit 1
fi

# Set Django settings for development
export DJANGO_SETTINGS_MODULE=api.settings.dev

# Default host and port
HOST=${1:-127.0.0.1}
PORT=${2:-8000}

echo -e "${GREEN}🔧 Using Django settings: $DJANGO_SETTINGS_MODULE${NC}"
echo -e "${GREEN}🌐 Server will be available at: http://$HOST:$PORT${NC}"
echo -e "${GREEN}🔄 Hot reloading enabled - admin panel will refresh automatically${NC}"
echo -e "${YELLOW}📝 Admin panel: http://$HOST:$PORT/admin${NC}"
echo -e "${YELLOW}🏥 Health check: http://$HOST:$PORT/health${NC}"
echo

# Start the development server with enhanced features
if command -v python manage.py runserver_plus > /dev/null 2>&1; then
    echo -e "${BLUE}🔥 Using runserver_plus for enhanced development experience${NC}"
    python manage.py runserver_plus \
        --print-sql \
        --threaded \
        --keep-meta-shutdown \
        $HOST:$PORT
else
    echo -e "${BLUE}🔥 Using standard runserver with hot reloading${NC}"
    python manage.py runserver_dev $HOST:$PORT
fi
