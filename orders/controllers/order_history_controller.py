from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404
from ninja.pagination import paginate
from ninja_extra import api_controller, http_get, http_post
from ninja_extra.permissions import IsAuthenticated

from api.decorators import handle_exceptions, log_api_call
from orders.models import (
    Order,
    OrderHistory,
)
from orders.schemas import OrderHistorySchema


@api_controller("/orders/{order_id}/history", tags=["Order History"])
class OrderHistoryController:
    permission_classes = [IsAuthenticated]

    @http_get("", response={200: list[OrderHistorySchema]})
    @handle_exceptions
    @log_api_call()
    @paginate
    def list_history(self, request, order_id: str):
        """Get paginated list of history entries for an order."""
        order = get_object_or_404(Order, id=order_id)
        history = (
            OrderHistory.objects.select_related("order", "created_by")
            .filter(order=order)
            .order_by("-created_at")
        )
        return 200, history

    @http_get("/{history_id}", response={200: OrderHistorySchema})
    @handle_exceptions
    @log_api_call()
    def get_history_entry(self, request, order_id: str, history_id: str):
        """Get single history entry by ID."""
        order = get_object_or_404(Order, id=order_id)
        history = get_object_or_404(
            OrderHistory.objects.select_related("order", "created_by"),
            id=history_id,
            order=order,
        )
        return 200, history

    @http_get("/status/{status}", response={200: list[OrderHistorySchema]})
    @handle_exceptions
    @log_api_call()
    @paginate
    def list_history_by_status(self, request, order_id: str, status: str):
        """Get paginated list of history entries for a specific status."""
        order = get_object_or_404(Order, id=order_id)
        history = (
            OrderHistory.objects.select_related("order", "created_by")
            .filter(order=order, status=status)
            .order_by("-created_at")
        )
        return 200, history

    @http_get("/status/{status}/count", response={200: dict})
    @handle_exceptions
    @log_api_call()
    def count_history_by_status(self, request, order_id: str, status: str):
        """Get count of history entries by status."""
        order = get_object_or_404(Order, id=order_id)
        count = OrderHistory.objects.filter(order=order, status=status).count()
        return 200, {"count": count, "status": status}

    @http_get("/summary", response={200: dict})
    @handle_exceptions
    @log_api_call()
    def get_history_summary(self, request, order_id: str):
        """Get history summary with counts by status."""
        order = get_object_or_404(Order, id=order_id)
        summary = (
            OrderHistory.objects.filter(order=order)
            .values("status")
            .annotate(count=Count("id"))
            .order_by("status")
        )
        total_entries = OrderHistory.objects.filter(order=order).count()
        return 200, {"summary": list(summary), "total": total_entries}

    @http_get("/timeline", response={200: list[OrderHistorySchema]})
    @handle_exceptions
    @log_api_call()
    def get_history_timeline(self, request, order_id: str):
        """Get complete history timeline for an order."""
        order = get_object_or_404(Order, id=order_id)
        timeline = (
            OrderHistory.objects.select_related("order", "created_by")
            .filter(order=order)
            .order_by("created_at")
        )
        return 200, timeline

    @http_post("", response={201: OrderHistorySchema})
    @handle_exceptions
    @log_api_call()
    @transaction.atomic
    def create_history_entry(self, request, order_id: str, note: str):
        """Create a new history entry for an order."""
        order = get_object_or_404(Order, id=order_id)

        history = OrderHistory.objects.create(
            order=order,
            status=order.status,
            note=note,
            created_by=request.user,
        )
        return 201, history
