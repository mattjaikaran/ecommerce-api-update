# Core App

## Overview
The Core app serves as the foundation of the ecommerce platform, providing essential functionality, base models, and utilities used throughout the application.

## Features
- User Authentication & Authorization
- Base Models
- Custom Management Commands
- Core Configurations
- Utility Functions

## Models

### AbstractBaseModel
Base model that all other models inherit from. Located in `core.models`.

```python
class AbstractBaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_created"
    )
    updated_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_updated"
    )
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)  # soft delete
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_deleted"
    )

    class Meta:
        abstract = True
        ordering = ["-created_at"]
```

### User Model
Extended Django User model with additional fields for ecommerce functionality.

## Management Commands

### create_superuser
Creates a superuser with predefined credentials from environment variables.
```bash
python manage.py create_superuser
```

### startapp_extended
Custom command to create a new Django app with pre-configured structure including controllers and schemas directories.
```bash
python manage.py startapp_extended app_name
```

## Directory Structure
```
core/
├── __init__.py
├── admin.py
├── apps.py
├── controllers/
│   ├── __init__.py
│   └── user_controller.py
├── management/
│   └── commands/
│       ├── create_superuser.py
│       └── startapp_extended.py
├── migrations/
├── models.py
├── schemas/
│   ├── __init__.py
│   └── user.py
├── tests/
│   └── __init__.py
└── utils/
    └── __init__.py
```

## Controllers

### UserController
Handles user-related operations using Django Ninja Extra.

```python
@api_controller("/users", tags=["Users"])
class UserController:
    @http_get("", response={200: List[UserSchema]})
    def get_users(self):
        try:
            users = User.objects.all()
            return 200, users
        except Exception as e:
            logger.error(f"Error fetching users: {e}")
            return 500, {"error": "An error occurred while fetching users", "message": str(e)}
```

## Schemas

### UserSchema
```python
class UserSchema(Schema):
    id: UUID
    email: str
    full_name: str
    is_active: bool
    created_at: datetime
    date_modified: datetime
```

## Authentication
- JWT-based authentication
- Token refresh mechanism
- Password reset functionality
- Email verification

## Utilities
- Custom exceptions
- Helper functions
- Common decorators
- Logging configuration

## Testing
```bash
# Run core app tests
python manage.py test core

# Run with coverage
coverage run manage.py test core
coverage report
```

## API Endpoints

### Authentication
- POST `/api/v1/auth/login/` - User login
- POST `/api/v1/auth/register/` - User registration
- POST `/api/v1/auth/refresh/` - Refresh token
- POST `/api/v1/auth/password-reset/` - Password reset

### Users
- GET `/api/v1/users/` - List users
- GET `/api/v1/users/{id}/` - Get user details
- PUT `/api/v1/users/{id}/` - Update user
- DELETE `/api/v1/users/{id}/` - Delete user

## Environment Variables
```env
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=your_secure_password
DJANGO_SUPERUSER_USERNAME=admin
```
