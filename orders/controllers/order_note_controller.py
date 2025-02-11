from django.db import transaction
from typing import List
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from ninja_extra import (
    api_controller,
    http_get,
    http_post,
    http_put,
    http_delete,
)
from ninja_extra.permissions import IsAuthenticated
from ninja.pagination import paginate

from orders.models import (
    Order,
    OrderNote,
)
from orders.schemas import (
    OrderNoteSchema,
    OrderNoteCreateSchema,
)


@api_controller("/orders/{order_id}/notes", tags=["Order Notes"])
class OrderNoteController:
    permission_classes = [IsAuthenticated]

    @http_get(
        "/",
        response={
            200: List[OrderNoteSchema],
            404: dict,
            500: dict,
        },
    )
    @paginate
    def list_notes(self, request, order_id: str):
        """Get a paginated list of notes for an order."""
        try:
            order = get_object_or_404(Order, id=order_id)
            notes = OrderNote.objects.select_related("order", "created_by").filter(
                order=order
            )

            # Filter notes based on user role
            if not request.user.is_staff:
                notes = notes.filter(is_customer_visible=True)

            return 200, notes.order_by("-created_at")
        except Order.DoesNotExist:
            return 404, {"error": "Order not found"}
        except Exception as e:
            return 500, {
                "error": "An error occurred while fetching notes",
                "message": str(e),
            }

    @http_get(
        "/{note_id}",
        response={
            200: OrderNoteSchema,
            404: dict,
            500: dict,
        },
    )
    def get_note(self, request, order_id: str, note_id: str):
        """Get a single note by ID."""
        try:
            order = get_object_or_404(Order, id=order_id)
            note = get_object_or_404(
                OrderNote.objects.select_related("order", "created_by"),
                id=note_id,
                order=order,
            )

            # Check visibility
            if not request.user.is_staff and not note.is_customer_visible:
                return 403, {"error": "You do not have permission to view this note"}

            return 200, note
        except Order.DoesNotExist:
            return 404, {"error": "Order not found"}
        except OrderNote.DoesNotExist:
            return 404, {"error": "Note not found"}
        except Exception as e:
            return 500, {
                "error": "An error occurred while fetching the note",
                "message": str(e),
            }

    @http_post(
        "",
        response={
            201: OrderNoteSchema,
            400: dict,
            404: dict,
            500: dict,
        },
    )
    @transaction.atomic
    def create_note(self, request, order_id: str, payload: OrderNoteCreateSchema):
        """Create a new note for an order."""
        try:
            order = get_object_or_404(Order, id=order_id)

            # Only staff can create non-customer-visible notes
            if not request.user.is_staff and not payload.is_customer_visible:
                return 403, {
                    "error": "You do not have permission to create private notes"
                }

            # Create note
            note = OrderNote.objects.create(
                order=order,
                note=payload.note,
                is_customer_visible=payload.is_customer_visible,
                created_by=request.user,
                meta_data=payload.meta_data,
            )

            return 201, note
        except Order.DoesNotExist:
            return 404, {"error": "Order not found"}
        except ValidationError as e:
            return 400, {"error": "Invalid data provided", "message": str(e)}
        except Exception as e:
            return 500, {
                "error": "An error occurred while creating the note",
                "message": str(e),
            }

    @http_put(
        "/{note_id}",
        response={
            200: OrderNoteSchema,
            400: dict,
            404: dict,
            500: dict,
        },
    )
    @transaction.atomic
    def update_note(
        self, request, order_id: str, note_id: str, payload: OrderNoteCreateSchema
    ):
        """Update an existing note."""
        try:
            order = get_object_or_404(Order, id=order_id)
            note = get_object_or_404(OrderNote, id=note_id, order=order)

            # Only staff or note creator can update notes
            if not request.user.is_staff and note.created_by != request.user:
                return 403, {"error": "You do not have permission to update this note"}

            # Only staff can update visibility
            if (
                not request.user.is_staff
                and payload.is_customer_visible != note.is_customer_visible
            ):
                return 403, {
                    "error": "You do not have permission to change note visibility"
                }

            # Update note
            note.note = payload.note
            note.is_customer_visible = payload.is_customer_visible
            note.meta_data = payload.meta_data
            note.save()

            return 200, note
        except Order.DoesNotExist:
            return 404, {"error": "Order not found"}
        except OrderNote.DoesNotExist:
            return 404, {"error": "Note not found"}
        except ValidationError as e:
            return 400, {"error": "Invalid data provided", "message": str(e)}
        except Exception as e:
            return 500, {
                "error": "An error occurred while updating the note",
                "message": str(e),
            }

    @http_delete(
        "/{note_id}",
        response={
            204: dict,
            404: dict,
            500: dict,
        },
    )
    @transaction.atomic
    def delete_note(self, request, order_id: str, note_id: str):
        """Delete a note."""
        try:
            order = get_object_or_404(Order, id=order_id)
            note = get_object_or_404(OrderNote, id=note_id, order=order)

            # Only staff or note creator can delete notes
            if not request.user.is_staff and note.created_by != request.user:
                return 403, {"error": "You do not have permission to delete this note"}

            note.delete()
            return 204, None
        except Order.DoesNotExist:
            return 404, {"error": "Order not found"}
        except OrderNote.DoesNotExist:
            return 404, {"error": "Note not found"}
        except Exception as e:
            return 500, {
                "error": "An error occurred while deleting the note",
                "message": str(e),
            }

    @http_get(
        "/customer",
        response={
            200: List[OrderNoteSchema],
            404: dict,
            500: dict,
        },
    )
    @paginate
    def list_customer_notes(self, request, order_id: str):
        """Get a paginated list of customer-visible notes for an order."""
        try:
            order = get_object_or_404(Order, id=order_id)
            notes = (
                OrderNote.objects.select_related("order", "created_by")
                .filter(order=order, is_customer_visible=True)
                .order_by("-created_at")
            )
            return 200, notes
        except Order.DoesNotExist:
            return 404, {"error": "Order not found"}
        except Exception as e:
            return 500, {
                "error": "An error occurred while fetching notes",
                "message": str(e),
            }

    @http_get(
        "/staff",
        response={
            200: List[OrderNoteSchema],
            404: dict,
            500: dict,
        },
    )
    @paginate
    def list_staff_notes(self, request, order_id: str):
        """Get a paginated list of staff-only notes for an order."""
        try:
            # Only staff can view staff notes
            if not request.user.is_staff:
                return 403, {"error": "You do not have permission to view staff notes"}

            order = get_object_or_404(Order, id=order_id)
            notes = (
                OrderNote.objects.select_related("order", "created_by")
                .filter(order=order, is_customer_visible=False)
                .order_by("-created_at")
            )
            return 200, notes
        except Order.DoesNotExist:
            return 404, {"error": "Order not found"}
        except Exception as e:
            return 500, {
                "error": "An error occurred while fetching notes",
                "message": str(e),
            }
