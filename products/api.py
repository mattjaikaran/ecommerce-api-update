# products/api.py
from ninja_extra import api_controller, http_get, http_post, http_put, http_delete
from .models import Products
from .schemas import ProductsSchema, ProductsCreateSchema

@api_controller('/products', tags=['Products'])
class ProductsAPI:
    @http_get('/', response=list[ProductsSchema])
    def list_products(self):
        return Products.objects.all()

    @http_post('/', response=ProductsSchema)
    def create_products(self, payload: ProductsCreateSchema):
        return Products.objects.create(**payload.dict())

    @http_get('/{id}', response=ProductsSchema)
    def get_products(self, id: str):
        return Products.objects.get(id=id)

    @http_put('/{id}', response=ProductsSchema)
    def update_products(self, id: str, payload: ProductsCreateSchema):
        products = Products.objects.get(id=id)
        for attr, value in payload.dict().items():
            setattr(products, attr, value)
        products.save()
        return products

    @http_delete('/{id}')
    def delete_products(self, id: str):
        Products.objects.get(id=id).delete()
        return {"success": True}
