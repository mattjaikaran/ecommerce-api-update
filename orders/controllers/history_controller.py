from django.db import transaction
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.db.models import Count
from ninja_extra import api_controller, route, http_get, http_post
from ninja_extra.permissions import IsAuthenticated
from ninja.pagination import paginate

from orders.models import (
    Order,
    OrderHistory,
)
from orders.schemas import (
    OrderHistorySchema,
)


@api_controller("/orders/{order_id}/history", tags=["Order History"])
class OrderHistoryController:
    permission_classes = [IsAuthenticated]

    @http_get("")
    @paginate
    def list_history(self, request, order_id: str):
        """Get a paginated list of history entries for an order."""
        try:
            order = get_object_or_404(Order, id=order_id)
            history = (
                OrderHistory.objects.select_related("order", "created_by")
                .filter(order=order)
                .order_by("-date_created")
            )
            return 200, history
        except Order.DoesNotExist:
            return 404, {"error": "Order not found"}
        except Exception as e:
            return 500, {
                "error": "An error occurred while fetching history",
                "message": str(e),
            }

    @http_get("/{history_id}")
    def get_history_entry(self, request, order_id: str, history_id: str):
        """Get a single history entry by ID."""
        try:
            order = get_object_or_404(Order, id=order_id)
            history = get_object_or_404(
                OrderHistory.objects.select_related("order", "created_by"),
                id=history_id,
                order=order,
            )
            return 200, history
        except Order.DoesNotExist:
            return 404, {"error": "Order not found"}
        except OrderHistory.DoesNotExist:
            return 404, {"error": "History entry not found"}
        except Exception as e:
            return 500, {
                "error": "An error occurred while fetching the history entry",
                "message": str(e),
            }

    @http_get("/status/{status}")
    @paginate
    def list_history_by_status(self, request, order_id: str, status: str):
        """Get a paginated list of history entries for a specific status."""
        try:
            order = get_object_or_404(Order, id=order_id)
            history = (
                OrderHistory.objects.select_related("order", "created_by")
                .filter(order=order, status=status)
                .order_by("-date_created")
            )
            return 200, history
        except Order.DoesNotExist:
            return 404, {"error": "Order not found"}
        except Exception as e:
            return 500, {
                "error": "An error occurred while fetching history",
                "message": str(e),
            }

    @http_get("/user/{user_id}")
    @paginate
    def list_history_by_user(self, request, order_id: str, user_id: str):
        """Get a paginated list of history entries for a specific user."""
        try:
            # Only staff can view history by user
            if not request.user.is_staff:
                return 403, {
                    "error": "You do not have permission to view history by user"
                }

            order = get_object_or_404(Order, id=order_id)
            history = (
                OrderHistory.objects.select_related("order", "created_by")
                .filter(order=order, created_by_id=user_id)
                .order_by("-date_created")
            )
            return 200, history
        except Order.DoesNotExist:
            return 404, {"error": "Order not found"}
        except Exception as e:
            return 500, {
                "error": "An error occurred while fetching history",
                "message": str(e),
            }

    @http_get("/date-range")
    @paginate
    def list_history_by_date_range(
        self, request, order_id: str, start_date: str, end_date: str
    ):
        """Get a paginated list of history entries within a date range."""
        try:
            order = get_object_or_404(Order, id=order_id)
            history = (
                OrderHistory.objects.select_related("order", "created_by")
                .filter(order=order, date_created__range=[start_date, end_date])
                .order_by("-date_created")
            )
            return 200, history
        except Order.DoesNotExist:
            return 404, {"error": "Order not found"}
        except Exception as e:
            return 500, {
                "error": "An error occurred while fetching history",
                "message": str(e),
            }

    @http_post("/add")
    @transaction.atomic
    def add_history_entry(self, request, order_id: str, status: str, notes: str = None):
        """Add a new history entry for an order."""
        try:
            # Only staff can add history entries
            if not request.user.is_staff:
                return 403, {
                    "error": "You do not have permission to add history entries"
                }

            order = get_object_or_404(Order, id=order_id)

            # Create history entry
            history = OrderHistory.objects.create(
                order=order,
                status=status,
                old_status=order.status,
                notes=notes,
                created_by=request.user,
                meta_data={},
            )

            # Update order status
            order.status = status
            order.save()

            return 201, history
        except Order.DoesNotExist:
            return 404, {"error": "Order not found"}
        except ValidationError as e:
            return 400, {"error": "Invalid data provided", "message": str(e)}
        except Exception as e:
            return 500, {
                "error": "An error occurred while adding history entry",
                "message": str(e),
            }

    @http_get("/summary")
    def get_history_summary(self, request, order_id: str):
        """Get a summary of order history."""
        try:
            order = get_object_or_404(Order, id=order_id)
            history = OrderHistory.objects.filter(order=order)

            # Calculate summary statistics
            summary = {
                "total_entries": history.count(),
                "status_changes": history.exclude(old_status=None).count(),
                "first_entry": history.order_by("date_created").first(),
                "last_entry": history.order_by("-date_created").first(),
                "status_breakdown": history.values("status").annotate(
                    count=Count("id")
                ),
                "user_breakdown": history.values("created_by__username").annotate(
                    count=Count("id")
                ),
            }

            return 200, summary
        except Order.DoesNotExist:
            return 404, {"error": "Order not found"}
        except Exception as e:
            return 500, {
                "error": "An error occurred while fetching history summary",
                "message": str(e),
            }
