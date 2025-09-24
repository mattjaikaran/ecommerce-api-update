from ninja_extra import api_controller, http_delete, http_get, http_post, http_put

from core.models import Address
from core.schemas import AddressCreateSchema, AddressSchema


@api_controller("/addresses", tags=["Addresses"])
class AddressController:
    @http_get("", response={200: list[AddressSchema], 404: dict, 500: dict})
    def list_addresses(self, request):
        try:
            addresses = Address.objects.filter(user=request.user)
            return 200, addresses
        except Exception as e:
            return 500, {"message": "Error listing addresses", "error": str(e)}

    @http_post("", response={201: AddressSchema, 400: dict, 500: dict})
    def create_address(self, request, payload: AddressCreateSchema):
        try:
            address = Address.objects.create(**payload.model_dump())
            return 201, address
        except Exception as e:
            return 500, {"message": "Error creating address", "error": str(e)}

    @http_put(
        "/{address_id}", response={200: AddressSchema, 400: dict, 404: dict, 500: dict}
    )
    def update_address(self, request, address_id: int, payload: AddressCreateSchema):
        try:
            address = Address.objects.get(id=address_id)
            address.update(**payload.model_dump())
            return 200, address
        except Address.DoesNotExist:
            return 404, {"message": "Address not found"}
        except Exception as e:
            return 500, {"message": "Error updating address", "error": str(e)}

    @http_delete("/{address_id}", response={204: dict, 404: dict, 500: dict})
    def delete_address(self, request, address_id: int):
        try:
            address = Address.objects.get(id=address_id)
            address.delete()
            return 204, {}
        except Address.DoesNotExist:
            return 404, {"message": "Address not found"}
        except Exception as e:
            return 500, {"message": "Error deleting address", "error": str(e)}
