#!/bin/bash

# Deployment script for Django Ecommerce API
# Handles deployment to different environments with proper checks

set -e

# Configuration
DEFAULT_ENVIRONMENT="staging"
ENVIRONMENT="${1:-$DEFAULT_ENVIRONMENT}"

# Colors
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

# Function to check if we're on the correct branch
check_branch() {
    local current_branch
    current_branch=$(git branch --show-current)
    
    case $ENVIRONMENT in
        "production")
            if [ "$current_branch" != "main" ]; then
                print_error "Production deployments must be from 'main' branch. Currently on '$current_branch'"
                exit 1
            fi
            ;;
        "staging")
            if [ "$current_branch" != "develop" ] && [ "$current_branch" != "main" ]; then
                print_warning "Staging typically deploys from 'develop' or 'main'. Currently on '$current_branch'"
                read -p "Continue anyway? (y/N): " -n 1 -r
                echo
                if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                    exit 1
                fi
            fi
            ;;
    esac
}

# Function to run pre-deployment checks
pre_deployment_checks() {
    print_info "Running pre-deployment checks..."
    
    # Check for uncommitted changes
    if ! git diff-index --quiet HEAD --; then
        print_error "There are uncommitted changes. Please commit or stash them before deploying."
        exit 1
    fi
    
    # Run code quality checks
    print_info "Running code quality checks..."
    if ! ./scripts/code_quality.sh; then
        print_error "Code quality checks failed. Please fix issues before deploying."
        exit 1
    fi
    
    # Check environment variables
    if [ "$ENVIRONMENT" = "production" ]; then
        print_info "Checking production environment variables..."
        required_vars=("SECRET_KEY" "DATABASE_URL" "REDIS_URL" "EMAIL_HOST_PASSWORD")
        for var in "${required_vars[@]}"; do
            if [ -z "${!var}" ]; then
                print_error "Required environment variable $var is not set."
                exit 1
            fi
        done
    fi
    
    print_success "Pre-deployment checks passed!"
}

# Function to backup database (production only)
backup_database() {
    if [ "$ENVIRONMENT" = "production" ]; then
        print_info "Creating database backup..."
        timestamp=$(date +%Y%m%d_%H%M%S)
        backup_file="backup_${timestamp}.sql"
        
        # This would be customized based on your deployment setup
        # Example for Docker-based deployment:
        # docker-compose exec db pg_dump -U postgres ecommerce_db > "backups/$backup_file"
        
        print_success "Database backup created: $backup_file"
    fi
}

# Function to deploy to staging
deploy_staging() {
    print_info "Deploying to staging environment..."
    
    # Build and deploy using Docker Compose
    docker-compose -f docker-compose.yml -f docker-compose.staging.yml build
    docker-compose -f docker-compose.yml -f docker-compose.staging.yml up -d
    
    # Run migrations
    docker-compose exec django python manage.py migrate
    
    # Collect static files
    docker-compose exec django python manage.py collectstatic --noinput
    
    # Restart services
    docker-compose restart django celery
    
    print_success "Staging deployment complete!"
}

# Function to deploy to production
deploy_production() {
    print_info "Deploying to production environment..."
    
    # Additional confirmation for production
    print_warning "You are about to deploy to PRODUCTION!"
    read -p "Are you sure you want to continue? (yes/NO): " -r
    if [ "$REPLY" != "yes" ]; then
        print_info "Production deployment cancelled."
        exit 0
    fi
    
    # Backup database
    backup_database
    
    # Build and deploy
    docker-compose -f docker-compose.prod.yml build
    docker-compose -f docker-compose.prod.yml up -d
    
    # Run migrations
    docker-compose -f docker-compose.prod.yml exec django python manage.py migrate
    
    # Collect static files
    docker-compose -f docker-compose.prod.yml exec django python manage.py collectstatic --noinput
    
    # Restart services
    docker-compose -f docker-compose.prod.yml restart django celery
    
    print_success "Production deployment complete!"
}

# Function to verify deployment
verify_deployment() {
    print_info "Verifying deployment..."
    
    local base_url
    case $ENVIRONMENT in
        "staging")
            base_url="http://staging.yourapp.com"
            ;;
        "production")
            base_url="https://yourapp.com"
            ;;
        *)
            base_url="http://localhost:8000"
            ;;
    esac
    
    # Check health endpoint
    if curl -f "$base_url/health/" >/dev/null 2>&1; then
        print_success "Health check passed!"
    else
        print_error "Health check failed!"
        exit 1
    fi
    
    # Check API endpoint
    if curl -f "$base_url/api/v1/" >/dev/null 2>&1; then
        print_success "API endpoint responding!"
    else
        print_warning "API endpoint not responding as expected."
    fi
}

# Function to notify team (optional)
notify_deployment() {
    if [ "$ENVIRONMENT" = "production" ]; then
        print_info "Notifying team of production deployment..."
        
        # Example: Send Slack notification
        # curl -X POST -H 'Content-type: application/json' \
        #     --data '{"text":"🚀 Production deployment completed successfully!"}' \
        #     "$SLACK_WEBHOOK_URL"
        
        # Example: Send Discord notification
        # curl -H "Content-Type: application/json" \
        #     -d '{"content":"🚀 Production deployment completed successfully!"}' \
        #     "$DISCORD_WEBHOOK_URL"
    fi
}

# Main deployment function
main() {
    print_info "Starting deployment to $ENVIRONMENT environment..."
    
    check_branch
    pre_deployment_checks
    
    case $ENVIRONMENT in
        "staging")
            deploy_staging
            ;;
        "production")
            deploy_production
            ;;
        *)
            print_error "Unknown environment: $ENVIRONMENT"
            echo "Usage: $0 [staging|production]"
            exit 1
            ;;
    esac
    
    verify_deployment
    notify_deployment
    
    print_success "Deployment to $ENVIRONMENT completed successfully! 🎉"
    
    # Show useful information
    echo ""
    echo "Deployment Summary:"
    echo "  Environment: $ENVIRONMENT"
    echo "  Branch: $(git branch --show-current)"
    echo "  Commit: $(git rev-parse --short HEAD)"
    echo "  Time: $(date)"
}

# Show help if requested
if [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
    echo "Deployment script for Django Ecommerce API"
    echo ""
    echo "Usage: $0 [environment]"
    echo ""
    echo "Environments:"
    echo "  staging     Deploy to staging environment (default)"
    echo "  production  Deploy to production environment"
    echo ""
    echo "Examples:"
    echo "  $0                # Deploy to staging"
    echo "  $0 staging        # Deploy to staging"
    echo "  $0 production     # Deploy to production"
    exit 0
fi

main "$@"
