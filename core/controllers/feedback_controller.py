from core.models import Feedback
from core.schemas import FeedbackSchema, FeedbackCreateSchema
from ninja_extra import api_controller, http_get, http_post, http_put, http_delete
from typing import List


@api_controller("/feedback", tags=["Feedback"])
class FeedbackController:

    @http_get("/feedback", response={200: List[FeedbackSchema], 400: dict, 500: dict})
    def list_feedback(self, request):
        try:
            feedback = Feedback.objects.all()
            return 200, feedback
        except Exception as e:
            return 500, {"message": "Error listing feedback", "error": str(e)}

    @http_post("/feedback", response={201: FeedbackSchema, 400: dict, 500: dict})
    def create_feedback(self, request, payload: FeedbackCreateSchema):
        try:
            feedback = Feedback.objects.create(**payload.model_dump())
            return 201, feedback
        except Exception as e:
            return 500, {"message": "Error creating feedback", "error": str(e)}

    @http_put(
        "/feedback/{feedback_id}",
        response={200: FeedbackSchema, 400: dict, 404: dict, 500: dict},
    )
    def update_feedback(self, request, feedback_id: int, payload: FeedbackCreateSchema):
        try:
            feedback = Feedback.objects.get(id=feedback_id)
            feedback.update(**payload.model_dump())
            return 200, feedback
        except Feedback.DoesNotExist:
            return 404, {"message": "Feedback not found"}
        except Exception as e:
            return 500, {"message": "Error updating feedback", "error": str(e)}

    @http_delete("/feedback/{feedback_id}", response={204: dict, 404: dict, 500: dict})
    def delete_feedback(self, request, feedback_id: int):
        try:
            feedback = Feedback.objects.get(id=feedback_id)
            feedback.delete()
            return 204, {}
        except Feedback.DoesNotExist:
            return 404, {"message": "Feedback not found"}
        except Exception as e:
            return 500, {"message": "Error deleting feedback", "error": str(e)}
