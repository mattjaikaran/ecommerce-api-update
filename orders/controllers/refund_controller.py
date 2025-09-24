from ninja_extra import api_controller, http_get, http_post

from orders.models import Refund
from orders.schemas import RefundCreateSchema, RefundSchema


@api_controller("/refunds", tags=["Refunds"])
class RefundController:
    @http_get("/", response={200: list[RefundSchema], 404: dict, 500: dict})
    def list_refunds(self, request):
        try:
            return 200, Refund.objects.all()
        except Refund.DoesNotExist:
            return 404, {"error": "Refunds not found"}
        except Exception as e:
            return 500, {"error": str(e)}

    @http_get("/{refund_id}", response={200: RefundSchema, 404: dict, 500: dict})
    def get_refund(self, request, refund_id: int):
        try:
            return 200, Refund.objects.get(id=refund_id)
        except Refund.DoesNotExist:
            return 404, {"error": "Refund not found"}
        except Exception as e:
            return 500, {"error get_refund": str(e)}

    @http_post("/", response={201: RefundSchema, 400: dict, 404: dict, 500: dict})
    def create_refund(self, request, payload: RefundCreateSchema):
        try:
            return 201, Refund.objects.create(**payload.model_dump())
        except Exception as e:
            return 500, {"error create_refund": str(e)}
