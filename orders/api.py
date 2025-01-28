# orders/api.py
from ninja_extra import api_controller, http_get, http_post, http_put, http_delete
from .models import Orders
from .schemas import OrdersSchema, OrdersCreateSchema

@api_controller('/orders', tags=['Orders'])
class OrdersAPI:
    @http_get('/', response=list[OrdersSchema])
    def list_orders(self):
        return Orders.objects.all()

    @http_post('/', response=OrdersSchema)
    def create_orders(self, payload: OrdersCreateSchema):
        return Orders.objects.create(**payload.dict())

    @http_get('/{id}', response=OrdersSchema)
    def get_orders(self, id: str):
        return Orders.objects.get(id=id)

    @http_put('/{id}', response=OrdersSchema)
    def update_orders(self, id: str, payload: OrdersCreateSchema):
        orders = Orders.objects.get(id=id)
        for attr, value in payload.dict().items():
            setattr(orders, attr, value)
        orders.save()
        return orders

    @http_delete('/{id}')
    def delete_orders(self, id: str):
        Orders.objects.get(id=id).delete()
        return {"success": True}
