from typing import List
from uuid import UUID
from ninja_extra import api_controller, http_get, http_post, http_put, http_delete
from ninja_extra.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from products.models import (
    Product,
    ProductAttribute,
    ProductAttributeGroup,
    ProductAttributeValue,
    ProductAttributeAssignment,
)
from products.schemas import (
    AttributeSchema,
    AttributeValueSchema,
    AttributeAssignmentSchema,
    AttributeCreateSchema,
    AttributeUpdateSchema,
    AttributeGroupSchema,
    AttributeGroupCreateSchema,
    AttributeGroupUpdateSchema,
    AttributeValueCreateSchema,
    AttributeValueUpdateSchema,
    AttributeAssignmentCreateSchema,
    ProductSchema,
    ProductAttributeGroupSchema,
)
import logging

logger = logging.getLogger(__name__)


@api_controller("/attributes", tags=["Attributes"], permissions=[IsAuthenticated])
class AttributeController:
    @http_get("", response={200: List[AttributeSchema]})
    def list_attributes(self):
        """List all product attributes"""
        try:
            attributes = ProductAttribute.objects.all()
            return 200, attributes
        except Exception as e:
            logger.error(f"Error fetching attributes: {e}")
            return 500, {
                "error": "An error occurred while fetching attributes",
                "message": str(e),
            }

    @http_get("/{attribute_id}", response={200: AttributeSchema})
    def get_attribute(self, attribute_id: UUID):
        """Get a specific product attribute"""
        try:
            attribute = get_object_or_404(ProductAttribute, id=attribute_id)
            return 200, attribute
        except Exception as e:
            logger.error(f"Error fetching attribute: {e}")
            return 500, {
                "error": "An error occurred while fetching attribute",
                "message": str(e),
            }

    @http_post("", response={201: AttributeSchema})
    def create_attribute(self, data: AttributeCreateSchema):
        """Create a new product attribute"""
        try:
            attribute = ProductAttribute.objects.create(
                name=data.name,
                code=data.code,
                description=data.description,
                is_filterable=data.is_filterable,
                position=data.position,
            )
            return 201, attribute
        except Exception as e:
            logger.error(f"Error creating attribute: {e}")
            return 500, {
                "error": "An error occurred while creating attribute",
                "message": str(e),
            }

    @http_put("/{attribute_id}", response={200: AttributeSchema})
    def update_attribute(self, attribute_id: UUID, data: AttributeUpdateSchema):
        """Update a product attribute"""
        try:
            attribute = get_object_or_404(ProductAttribute, id=attribute_id)

            for field, value in data.dict(exclude_unset=True).items():
                setattr(attribute, field, value)

            attribute.save()
            return 200, attribute
        except Exception as e:
            logger.error(f"Error updating attribute: {e}")
            return 500, {
                "error": "An error occurred while updating attribute",
                "message": str(e),
            }

    @http_delete("/{attribute_id}", response={204: None})
    def delete_attribute(self, attribute_id: UUID):
        """Delete a product attribute"""
        try:
            attribute = get_object_or_404(ProductAttribute, id=attribute_id)
            attribute.delete()
            return 204, None
        except Exception as e:
            logger.error(f"Error deleting attribute: {e}")
            return 500, {
                "error": "An error occurred while deleting attribute",
                "message": str(e),
            }

    @http_get("/{attribute_id}/values", response={200: List[AttributeValueSchema]})
    def list_attribute_values(self, attribute_id: UUID):
        """List all values for a specific attribute"""
        try:
            values = ProductAttributeValue.objects.filter(attribute_id=attribute_id)
            return 200, values
        except Exception as e:
            logger.error(f"Error fetching attribute values: {e}")
            return 500, {
                "error": "An error occurred while fetching attribute values",
                "message": str(e),
            }

    @http_post("/{attribute_id}/values", response={201: AttributeValueSchema})
    def create_attribute_value(
        self, attribute_id: UUID, data: AttributeValueCreateSchema
    ):
        """Create a new value for a specific attribute"""
        try:
            attribute = get_object_or_404(ProductAttribute, id=attribute_id)
            value = ProductAttributeValue.objects.create(
                attribute=attribute, value=data.value, position=data.position
            )
            return 201, value
        except Exception as e:
            logger.error(f"Error creating attribute value: {e}")
            return 500, {
                "error": "An error occurred while creating attribute value",
                "message": str(e),
            }

    @http_put("/{attribute_id}/values/{value_id}", response={200: AttributeValueSchema})
    def update_attribute_value(
        self, attribute_id: UUID, value_id: UUID, data: AttributeValueUpdateSchema
    ):
        """Update a specific attribute value"""
        try:
            value = get_object_or_404(
                ProductAttributeValue, id=value_id, attribute_id=attribute_id
            )

            for field, val in data.dict(exclude_unset=True).items():
                setattr(value, field, val)

            value.save()
            return 200, value
        except Exception as e:
            logger.error(f"Error updating attribute value: {e}")
            return 500, {
                "error": "An error occurred while updating attribute value",
                "message": str(e),
            }

    @http_delete("/{attribute_id}/values/{value_id}", response={204: None})
    def delete_attribute_value(self, attribute_id: UUID, value_id: UUID):
        """Delete a specific attribute value"""
        try:
            value = get_object_or_404(
                ProductAttributeValue, id=value_id, attribute_id=attribute_id
            )
            value.delete()
            return 204, None
        except Exception as e:
            logger.error(f"Error deleting attribute value: {e}")
            return 500, {
                "error": "An error occurred while deleting attribute value",
                "message": str(e),
            }

    @http_get("/products/{product_id}", response={200: List[AttributeAssignmentSchema]})
    def list_product_attributes(self, product_id: UUID):
        """List all attributes assigned to a product"""
        try:
            assignments = ProductAttributeAssignment.objects.filter(
                product_id=product_id
            )
            return 200, assignments
        except Exception as e:
            logger.error(f"Error fetching product attributes: {e}")
            return 500, {
                "error": "An error occurred while fetching product attributes",
                "message": str(e),
            }

    @http_post(
        "/products/{product_id}/assign", response={201: AttributeAssignmentSchema}
    )
    def assign_attribute(self, product_id: UUID, data: AttributeAssignmentCreateSchema):
        """Assign an attribute value to a product"""
        try:
            product = get_object_or_404(Product, id=product_id)
            attribute = get_object_or_404(ProductAttribute, id=data.attribute_id)
            value = get_object_or_404(ProductAttributeValue, id=data.value_id)

            assignment = ProductAttributeAssignment.objects.create(
                product=product, attribute=attribute, value=value
            )
            return 201, assignment
        except Exception as e:
            logger.error(f"Error assigning attribute: {e}")
            return 500, {
                "error": "An error occurred while assigning attribute",
                "message": str(e),
            }

    @http_delete(
        "/products/{product_id}/attributes/{attribute_id}", response={204: None}
    )
    def remove_attribute(self, product_id: UUID, attribute_id: UUID):
        """Remove an attribute assignment from a product"""
        try:
            assignment = get_object_or_404(
                ProductAttributeAssignment,
                product_id=product_id,
                attribute_id=attribute_id,
            )
            assignment.delete()
            return 204, None
        except Exception as e:
            logger.error(f"Error removing attribute: {e}")
            return 500, {
                "error": "An error occurred while removing attribute",
                "message": str(e),
            }

    @http_get("/groups", response={200: List[AttributeGroupSchema]})
    def list_attribute_groups(self):
        """List all attribute groups"""
        try:
            groups = ProductAttributeGroup.objects.all()
            return 200, groups
        except Exception as e:
            logger.error(f"Error fetching attribute groups: {e}")
            return 500, {
                "error": "An error occurred while fetching attribute groups",
                "message": str(e),
            }

    @http_post("/groups", response={201: AttributeGroupSchema})
    def create_attribute_group(self, data: AttributeGroupCreateSchema):
        """Create a new attribute group"""
        try:
            group = ProductAttributeGroup.objects.create(
                name=data.name,
                description=data.description,
                position=data.position,
            )
            return 201, group
        except Exception as e:
            logger.error(f"Error creating attribute group: {e}")
            return 500, {
                "error": "An error occurred while creating attribute group",
                "message": str(e),
            }

    @http_put("/groups/{group_id}", response={200: AttributeGroupSchema})
    def update_attribute_group(self, group_id: UUID, data: AttributeGroupUpdateSchema):
        """Update an attribute group"""
        try:
            group = get_object_or_404(ProductAttributeGroup, id=group_id)
            for field, value in data.dict(exclude_unset=True).items():
                setattr(group, field, value)
            group.save()
            return 200, group
        except Exception as e:
            logger.error(f"Error updating attribute group: {e}")
            return 500, {
                "error": "An error occurred while updating attribute group",
                "message": str(e),
            }

    @http_delete("/groups/{group_id}", response={204: None})
    def delete_attribute_group(self, group_id: UUID):
        """Delete an attribute group"""
        try:
            group = get_object_or_404(ProductAttributeGroup, id=group_id)
            group.delete()
            return 204, None
        except Exception as e:
            logger.error(f"Error deleting attribute group: {e}")
            return 500, {
                "error": "An error occurred while deleting attribute group",
                "message": str(e),
            }

    @http_post("/groups/{group_id}/attributes", response={201: AttributeGroupSchema})
    def add_attributes_to_group(self, group_id: UUID, data: AttributeGroupUpdateSchema):
        """Add attributes to an attribute group"""
        try:
            group = get_object_or_404(ProductAttributeGroup, id=group_id)
            for attribute_id in data.attribute_ids:
                attribute = get_object_or_404(ProductAttribute, id=attribute_id)
                group.attributes.add(attribute)
            group.save()
            return 201, group
        except Exception as e:
            logger.error(f"Error adding attributes to group: {e}")
            return 500, {
                "error": "An error occurred while adding attributes to group",
                "message": str(e),
            }

    @http_delete("/groups/{group_id}/attributes", response={204: None})
    def remove_attributes_from_group(
        self, group_id: UUID, data: AttributeGroupUpdateSchema
    ):
        """Remove attributes from an attribute group"""
        try:
            group = get_object_or_404(ProductAttributeGroup, id=group_id)
            for attribute_id in data.attribute_ids:
                attribute = get_object_or_404(ProductAttribute, id=attribute_id)
                group.attributes.remove(attribute)
            group.save()
            return 204, None
        except Exception as e:
            logger.error(f"Error removing attributes from group: {e}")
            return 500, {
                "error": "An error occurred while removing attributes from group",
                "message": str(e),
            }

    @http_get("/groups/{group_id}/attributes", response={200: List[AttributeSchema]})
    def list_attributes_in_group(self, group_id: UUID):
        """List all attributes in a specific attribute group"""
        try:
            group = get_object_or_404(ProductAttributeGroup, id=group_id)
            attributes = group.attributes.all()
            return 200, attributes
        except Exception as e:
            logger.error(f"Error fetching attributes in group: {e}")
            return 500, {
                "error": "An error occurred while fetching attributes in group",
                "message": str(e),
            }

    @http_get("/groups/{group_id}/products", response={200: List[ProductSchema]})
    def list_products_in_group(self, group_id: UUID):
        """List all products in a specific attribute group"""
        try:
            group = get_object_or_404(ProductAttributeGroup, id=group_id)
            products = group.products.all()
            return 200, products
        except Exception as e:
            logger.error(f"Error fetching products in group: {e}")
            return 500, {
                "error": "An error occurred while fetching products in group",
                "message": str(e),
            }
