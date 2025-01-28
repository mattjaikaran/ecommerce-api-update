from django.urls import path
from ninja_extra import NinjaExtraAPI
from orders.controllers.order_controller import OrderController
from orders.controllers.fulfillment_controller import FulfillmentController
from orders.controllers.payment_controller import PaymentController
from orders.controllers.tax_controller import TaxController
from orders.controllers.note_controller import OrderNoteController
from orders.controllers.history_controller import OrderHistoryController

api = NinjaExtraAPI(
    title="Orders API", version="1.0.0", description="API for managing orders"
)

# Register controllers
api.register_controllers(
    OrderController,
    FulfillmentController,
    PaymentController,
    TaxController,
    OrderNoteController,
    OrderHistoryController,
)

urlpatterns = [
    path("api/", api.urls),
]
