from ninja_extra import api_controller, http_get

from payments.schemas import PaymentMethodSchema


@api_controller("/payments", tags=["payments"])
class PaymentController:
    def get_payment_methods(self):
        pass

    @http_get("/{payment_method_id}", response={200: PaymentMethodSchema, 500: dict})
    def get_payment_method(self, payment_method_id: str):
        pass

    def create_payment_method(self, payment_method_data: dict):
        pass
