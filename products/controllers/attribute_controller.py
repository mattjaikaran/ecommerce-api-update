import logging
from uuid import UUID

from django.shortcuts import get_object_or_404
from ninja.pagination import paginate
from ninja_extra import api_controller, http_delete, http_get, http_post, http_put
from ninja_extra.permissions import IsAuthenticated

from api.decorators import handle_exceptions, log_api_call
from products.models import (
    Product,
    ProductAttribute,
    ProductAttributeAssignment,
    ProductAttributeGroup,
    ProductAttributeValue,
)
from products.schemas import (
    AttributeAssignmentCreateSchema,
    AttributeAssignmentSchema,
    AttributeCreateSchema,
    AttributeGroupCreateSchema,
    AttributeGroupSchema,
    AttributeGroupUpdateSchema,
    AttributeSchema,
    AttributeUpdateSchema,
    AttributeValueCreateSchema,
    AttributeValueSchema,
    AttributeValueUpdateSchema,
)

logger = logging.getLogger(__name__)


@api_controller("/products/attributes", tags=["Product Attributes"])
class AttributeController:
    permission_classes = [IsAuthenticated]

    @http_get("", response={200: list[AttributeSchema]})
    @handle_exceptions
    @log_api_call()
    @paginate
    def list_attributes(self, request):
        """Get paginated list of attributes."""
        attributes = ProductAttribute.objects.order_by("position", "name")
        return 200, attributes

    @http_get("/{id}", response={200: AttributeSchema})
    @handle_exceptions
    @log_api_call()
    def get_attribute(self, request, id: UUID):
        """Get attribute by ID."""
        attribute = get_object_or_404(ProductAttribute, id=id)
        return 200, attribute

    @http_post("", response={201: AttributeSchema})
    @handle_exceptions
    @log_api_call()
    def create_attribute(self, request, data: AttributeCreateSchema):
        """Create new product attribute."""
        attribute = ProductAttribute.objects.create(
            name=data.name,
            code=data.code,
            description=data.description,
            is_filterable=data.is_filterable,
            position=data.position,
        )
        return 201, attribute

    @http_put("/{attribute_id}", response={200: AttributeSchema})
    @handle_exceptions
    @log_api_call()
    def update_attribute(
        self, request, attribute_id: UUID, data: AttributeUpdateSchema
    ):
        """Update product attribute."""
        attribute = get_object_or_404(ProductAttribute, id=attribute_id)
        for field, value in data.dict(exclude_unset=True).items():
            setattr(attribute, field, value)
        attribute.save()
        return 200, attribute

    @http_delete("/{attribute_id}", response={204: None})
    @handle_exceptions
    @log_api_call()
    def delete_attribute(self, request, attribute_id: UUID):
        """Delete product attribute."""
        attribute = get_object_or_404(ProductAttribute, id=attribute_id)
        attribute.delete()
        return 204, None

    @http_get("/{attribute_id}/values", response={200: list[AttributeValueSchema]})
    @handle_exceptions
    @log_api_call()
    @paginate
    def list_attribute_values(self, request, attribute_id: UUID):
        """List all values for a specific attribute."""
        values = ProductAttributeValue.objects.filter(
            attribute_id=attribute_id
        ).order_by("position", "value")
        return 200, values

    @http_post("/{attribute_id}/values", response={201: AttributeValueSchema})
    @handle_exceptions
    @log_api_call()
    def create_attribute_value(
        self, request, attribute_id: UUID, data: AttributeValueCreateSchema
    ):
        """Create new value for a specific attribute."""
        attribute = get_object_or_404(ProductAttribute, id=attribute_id)
        value = ProductAttributeValue.objects.create(
            attribute=attribute, value=data.value, position=data.position
        )
        return 201, value

    @http_put("/{attribute_id}/values/{value_id}", response={200: AttributeValueSchema})
    @handle_exceptions
    @log_api_call()
    def update_attribute_value(
        self,
        request,
        attribute_id: UUID,
        value_id: UUID,
        data: AttributeValueUpdateSchema,
    ):
        """Update specific attribute value."""
        value = get_object_or_404(
            ProductAttributeValue, id=value_id, attribute_id=attribute_id
        )
        for field, val in data.dict(exclude_unset=True).items():
            setattr(value, field, val)
        value.save()
        return 200, value

    @http_delete("/{attribute_id}/values/{value_id}", response={204: None})
    @handle_exceptions
    @log_api_call()
    def delete_attribute_value(self, request, attribute_id: UUID, value_id: UUID):
        """Delete specific attribute value."""
        value = get_object_or_404(
            ProductAttributeValue, id=value_id, attribute_id=attribute_id
        )
        value.delete()
        return 204, None

    @http_get("/products/{product_id}", response={200: list[AttributeAssignmentSchema]})
    @handle_exceptions
    @log_api_call()
    @paginate
    def list_product_attributes(self, request, product_id: UUID):
        """List all attributes assigned to a product."""
        assignments = ProductAttributeAssignment.objects.filter(
            product_id=product_id
        ).select_related("attribute", "value")
        return 200, assignments

    @http_post(
        "/products/{product_id}/assign", response={201: AttributeAssignmentSchema}
    )
    @handle_exceptions
    @log_api_call()
    def assign_attribute(
        self, request, product_id: UUID, data: AttributeAssignmentCreateSchema
    ):
        """Assign attribute value to a product."""
        product = get_object_or_404(Product, id=product_id)
        attribute = get_object_or_404(ProductAttribute, id=data.attribute_id)
        value = get_object_or_404(ProductAttributeValue, id=data.value_id)

        assignment = ProductAttributeAssignment.objects.create(
            product=product, attribute=attribute, value=value
        )
        return 201, assignment

    @http_delete(
        "/products/{product_id}/attributes/{attribute_id}", response={204: None}
    )
    @handle_exceptions
    @log_api_call()
    def remove_attribute(self, request, product_id: UUID, attribute_id: UUID):
        """Remove attribute assignment from a product."""
        assignment = get_object_or_404(
            ProductAttributeAssignment,
            product_id=product_id,
            attribute_id=attribute_id,
        )
        assignment.delete()
        return 204, None

    @http_get("/groups", response={200: list[AttributeGroupSchema]})
    @handle_exceptions
    @log_api_call()
    @paginate
    def list_attribute_groups(self, request):
        """List all attribute groups."""
        groups = ProductAttributeGroup.objects.order_by("position", "name")
        return 200, groups

    @http_post("/groups", response={201: AttributeGroupSchema})
    @handle_exceptions
    @log_api_call()
    def create_attribute_group(self, request, data: AttributeGroupCreateSchema):
        """Create new attribute group."""
        group = ProductAttributeGroup.objects.create(
            name=data.name,
            description=data.description,
            position=data.position,
        )
        return 201, group

    @http_put("/groups/{group_id}", response={200: AttributeGroupSchema})
    @handle_exceptions
    @log_api_call()
    def update_attribute_group(
        self, request, group_id: UUID, data: AttributeGroupUpdateSchema
    ):
        """Update attribute group."""
        group = get_object_or_404(ProductAttributeGroup, id=group_id)
        for field, value in data.dict(exclude_unset=True).items():
            setattr(group, field, value)
        group.save()
        return 200, group

    @http_delete("/groups/{group_id}", response={204: None})
    @handle_exceptions
    @log_api_call()
    def delete_attribute_group(self, request, group_id: UUID):
        """Delete attribute group."""
        group = get_object_or_404(ProductAttributeGroup, id=group_id)
        group.delete()
        return 204, None
