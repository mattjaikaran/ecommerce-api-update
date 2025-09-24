import logging
from uuid import UUID

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from ninja_extra import api_controller, http_delete, http_get, http_post, http_put
from ninja_jwt.tokens import RefreshToken

from core.schemas import (
    UserLoginSchema,
    UserSchema,
    UserSignupSchema,
    UserUpdateSchema,
)

logger = logging.getLogger(__name__)

User = get_user_model()


@api_controller("/users", tags=["Users"])
class UserController:
    @http_post("/signup", response={201: UserSchema, 400: dict, 500: dict})
    def signup(self, request, data: UserSignupSchema):
        """Create a new user account"""
        try:
            # Check if username exists
            if User.objects.filter(username=data.username).exists():
                return 400, {"error": "A user with this username already exists."}

            # Check if email exists
            if User.objects.filter(email=data.email).exists():
                return 400, {"error": "A user with this email already exists."}

            # Validate password
            try:
                validate_password(data.password)
            except ValidationError as e:
                return 400, {"error": e.messages}

            # Create user
            user = User.objects.create_user(
                username=data.username,
                email=data.email,
                password=data.password,
                first_name=data.first_name,
                last_name=data.last_name,
                is_staff=False,
                is_superuser=False,
            )
            return 201, UserSchema.from_orm(user)
        except ValidationError as e:
            return 400, {"error": e.messages}
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            return 500, {
                "error": "An error occurred while creating user",
                "message": str(e),
            }

    @http_post("/login", response={200: dict, 400: dict})
    def login(self, request, data: UserLoginSchema):
        try:
            user = authenticate(username=data.username, password=data.password)
            if not user:
                return 400, {"error": "Invalid credentials"}

            # Generate token
            refresh = RefreshToken.for_user(user)
            return 200, {
                "token": str(refresh.access_token),
                "refresh": str(refresh),
                "user": UserSchema.from_orm(user).dict(),
            }
        except Exception as e:
            return 400, {"error": str(e)}

    @http_get("", response={200: list[UserSchema], 500: dict})
    def list_users(self, request):
        try:
            users = User.objects.all()
            return 200, [UserSchema.from_orm(user) for user in users]
        except Exception as e:
            logger.error(f"Error listing users: {e}")
            return 500, {
                "error": "An error occurred while listing users",
                "message": str(e),
            }

    @http_get("/me", response={200: UserSchema, 401: dict, 500: dict})
    def get_current_user(self, request):
        """Get the current authenticated user"""
        try:
            if request.user.is_authenticated:
                return 200, UserSchema.from_orm(request.user)
            return 401, {"error": "Not authenticated"}
        except Exception as e:
            logger.error(f"Error getting current user: {e}")
            return 500, {
                "error": "An error occurred while getting current user",
                "message": str(e),
            }

    @http_get("/{user_id}", response={200: UserSchema, 404: dict, 500: dict})
    def get_user(self, request, user_id: UUID):
        try:
            user = get_object_or_404(User, id=user_id)
            return 200, UserSchema.from_orm(user)
        except User.DoesNotExist:
            return 404, {"error": "User not found"}
        except Exception as e:
            logger.error(f"Error getting user {user_id}: {e}")
            return 500, {
                "error": "An error occurred while getting user",
                "message": str(e),
            }

    @http_put("/{user_id}", response={200: UserSchema, 400: dict, 404: dict, 500: dict})
    def update_user(self, request, user_id: UUID, payload: UserUpdateSchema):
        try:
            user = get_object_or_404(User, id=user_id)
            for attr, value in payload.dict(exclude_unset=True).items():
                setattr(user, attr, value)
            user.save()
            return 200, UserSchema.from_orm(user)
        except User.DoesNotExist:
            return 404, {"error": "User not found"}
        except Exception as e:
            logger.error(f"Error updating user {user_id}: {e}")
            return 500, {
                "error": "An error occurred while updating user",
                "message": str(e),
            }

    @http_delete("/{user_id}", response={204: None, 404: dict, 500: dict})
    def delete_user(self, request, user_id: UUID):
        try:
            user = get_object_or_404(User, id=user_id)
            user.delete()
            return 204, None
        except User.DoesNotExist:
            return 404, {"error": "User not found"}
        except Exception as e:
            logger.error(f"Error deleting user {user_id}: {e}")
            return 500, {
                "error": "An error occurred while deleting user",
                "message": str(e),
            }
