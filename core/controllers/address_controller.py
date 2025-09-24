from django.shortcuts import get_object_or_404
from ninja.pagination import paginate
from ninja_extra import api_controller, http_delete, http_get, http_post, http_put
from ninja_extra.permissions import IsAuthenticated

from api.decorators import handle_exceptions, log_api_call
from core.models import Address
from core.schemas import AddressCreateSchema, AddressSchema


@api_controller("/addresses", tags=["Addresses"])
class AddressController:
    permission_classes = [IsAuthenticated]

    @http_get("", response={200: list[AddressSchema]})
    @handle_exceptions
    @log_api_call()
    @paginate
    def list_addresses(self, request):
        """Get paginated list of user addresses."""
        addresses = Address.objects.filter(user=request.user).order_by("-created_at")
        return 200, addresses

    @http_get("/{address_id}", response={200: AddressSchema})
    @handle_exceptions
    @log_api_call()
    def get_address(self, request, address_id: int):
        """Get specific address by ID."""
        address = get_object_or_404(Address, id=address_id, user=request.user)
        return 200, address

    @http_post("", response={201: AddressSchema})
    @handle_exceptions
    @log_api_call()
    def create_address(self, request, payload: AddressCreateSchema):
        """Create new address for authenticated user."""
        address_data = payload.model_dump()
        address_data["user"] = request.user
        address = Address.objects.create(**address_data)
        return 201, address

    @http_put("/{address_id}", response={200: AddressSchema})
    @handle_exceptions
    @log_api_call()
    def update_address(self, request, address_id: int, payload: AddressCreateSchema):
        """Update existing user address."""
        address = get_object_or_404(Address, id=address_id, user=request.user)
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(address, field, value)
        address.save()
        return 200, address

    @http_delete("/{address_id}", response={204: None})
    @handle_exceptions
    @log_api_call()
    def delete_address(self, request, address_id: int):
        """Delete user address."""
        address = get_object_or_404(Address, id=address_id, user=request.user)
        address.delete()
        return 204, None
