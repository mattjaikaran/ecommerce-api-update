from django.shortcuts import get_object_or_404
from ninja.pagination import paginate
from ninja_extra import api_controller, http_get, http_post
from ninja_extra.permissions import IsAuthenticated

from api.decorators import handle_exceptions, log_api_call
from orders.models import Refund
from orders.schemas import RefundCreateSchema, RefundSchema


@api_controller("/refunds", tags=["Refunds"])
class RefundController:
    permission_classes = [IsAuthenticated]

    @http_get("", response={200: list[RefundSchema]})
    @handle_exceptions
    @log_api_call()
    @paginate
    def list_refunds(self, request):
        """Get paginated list of refunds."""
        refunds = Refund.objects.select_related("order").order_by("-created_at")
        return 200, refunds

    @http_get("/{refund_id}", response={200: RefundSchema})
    @handle_exceptions
    @log_api_call()
    def get_refund(self, request, refund_id: int):
        """Get specific refund by ID."""
        refund = get_object_or_404(Refund.objects.select_related("order"), id=refund_id)
        return 200, refund

    @http_post("", response={201: RefundSchema})
    @handle_exceptions
    @log_api_call()
    def create_refund(self, request, payload: RefundCreateSchema):
        """Create new refund."""
        refund = Refund.objects.create(**payload.model_dump())
        return 201, refund
