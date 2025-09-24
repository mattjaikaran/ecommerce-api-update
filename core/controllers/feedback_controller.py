from django.shortcuts import get_object_or_404
from ninja.pagination import paginate
from ninja_extra import api_controller, http_delete, http_get, http_post, http_put
from ninja_extra.permissions import IsAuthenticated

from api.decorators import handle_exceptions, log_api_call
from core.models import CustomerFeedback
from core.schemas import CustomerFeedbackCreateSchema, CustomerFeedbackSchema


@api_controller("/feedback", tags=["Feedback"])
class FeedbackController:
    permission_classes = [IsAuthenticated]

    @http_get("", response={200: list[CustomerFeedbackSchema]})
    @handle_exceptions
    @log_api_call()
    @paginate
    def list_feedback(self, request):
        """Get paginated list of customer feedback."""
        feedback = CustomerFeedback.objects.select_related("customer").all()
        return 200, feedback

    @http_post("", response={201: CustomerFeedbackSchema})
    @handle_exceptions
    @log_api_call()
    def create_feedback(self, request, payload: CustomerFeedbackCreateSchema):
        """Create new customer feedback."""
        feedback = CustomerFeedback.objects.create(**payload.model_dump())
        return 201, feedback

    @http_put("/{feedback_id}", response={200: CustomerFeedbackSchema})
    @handle_exceptions
    @log_api_call()
    def update_feedback(
        self, request, feedback_id: int, payload: CustomerFeedbackCreateSchema
    ):
        """Update existing customer feedback."""
        feedback = get_object_or_404(CustomerFeedback, id=feedback_id)
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(feedback, field, value)
        feedback.save()
        return 200, feedback

    @http_delete("/{feedback_id}", response={204: None})
    @handle_exceptions
    @log_api_call()
    def delete_feedback(self, request, feedback_id: int):
        """Delete customer feedback."""
        feedback = get_object_or_404(CustomerFeedback, id=feedback_id)
        feedback.delete()
        return 204, None
