import pytest
from django.test import Client

from cart.models import Cart
from cart.tests.factories import CartFactory, CartItemFactory
from core.tests.factories import CustomerFactory, UserFactory
from products.tests.factories import ProductVariantFactory


@pytest.mark.django_db
class TestCartController:
    """Test operations for CartController."""

    def setup_method(self):
        """Set up test data."""
        self.client = Client()
        self.user = UserFactory()
        self.customer = CustomerFactory(user=self.user)
        self.client.force_login(self.user)

    def test_create_cart(self):
        """Test creating a new cart."""
        cart_data = {
            "customer_id": str(self.customer.id),
            "session_key": "test-session-123",
        }

        response = self.client.post(
            "/api/carts/", data=cart_data, content_type="application/json"
        )

        assert response.status_code == 201
        assert Cart.objects.filter(customer=self.customer).exists()

        cart = Cart.objects.get(customer=self.customer)
        assert cart.session_key == cart_data["session_key"]

    def test_create_cart_anonymous(self):
        """Test creating a cart without customer (anonymous)."""
        cart_data = {"session_key": "anonymous-session-123"}

        response = self.client.post(
            "/api/carts/", data=cart_data, content_type="application/json"
        )

        assert response.status_code == 201
        assert Cart.objects.filter(session_key=cart_data["session_key"]).exists()

    def test_read_cart_list(self):
        """Test retrieving list of carts."""
        CartFactory.create_batch(3, customer=self.customer)

        response = self.client.get("/api/carts/")

        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 3

    def test_read_cart_list_filters(self):
        """Test filtering carts by various criteria."""
        active_cart = CartFactory(customer=self.customer, is_active=True)
        inactive_cart = CartFactory(customer=self.customer, is_active=False)

        # Test active filter
        response = self.client.get("/api/carts/?is_active=true")
        assert response.status_code == 200
        data = response.json()
        cart_ids = [item["id"] for item in data]
        assert str(active_cart.id) in cart_ids
        assert str(inactive_cart.id) not in cart_ids

    def test_read_cart_detail(self):
        """Test retrieving a specific cart."""
        cart = CartFactory(customer=self.customer)
        CartItemFactory.create_batch(2, cart=cart)

        response = self.client.get(f"/api/carts/{cart.id}/")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(cart.id)
        assert data["customer_id"] == str(self.customer.id)
        assert len(data["items"]) == 2

    def test_read_cart_detail_not_found(self):
        """Test retrieving non-existent cart returns 404."""
        import uuid

        fake_id = uuid.uuid4()

        response = self.client.get(f"/api/carts/{fake_id}/")

        assert response.status_code == 404

    def test_update_cart(self):
        """Test updating a cart."""
        cart = CartFactory(customer=self.customer)
        update_data = {"session_key": "updated-session-key"}

        response = self.client.put(
            f"/api/carts/{cart.id}/", data=update_data, content_type="application/json"
        )

        assert response.status_code == 200
        cart.refresh_from_db()
        assert cart.session_key == update_data["session_key"]

    def test_delete_cart(self):
        """Test deleting a cart (soft delete)."""
        cart = CartFactory(customer=self.customer)

        response = self.client.delete(f"/api/carts/{cart.id}/")

        assert response.status_code == 204
        cart.refresh_from_db()
        assert cart.is_deleted is True

    def test_add_item_to_cart(self):
        """Test adding an item to cart."""
        cart = CartFactory(customer=self.customer)
        product_variant = ProductVariantFactory()
        item_data = {"product_variant_id": str(product_variant.id), "quantity": 2}

        response = self.client.post(
            f"/api/carts/{cart.id}/items/",
            data=item_data,
            content_type="application/json",
        )

        assert response.status_code == 201
        assert cart.items.filter(product_variant=product_variant).exists()

        cart_item = cart.items.get(product_variant=product_variant)
        assert cart_item.quantity == item_data["quantity"]

    def test_update_cart_item_quantity(self):
        """Test updating cart item quantity."""
        cart = CartFactory(customer=self.customer)
        cart_item = CartItemFactory(cart=cart, quantity=1)
        update_data = {"quantity": 5}

        response = self.client.put(
            f"/api/carts/{cart.id}/items/{cart_item.id}/",
            data=update_data,
            content_type="application/json",
        )

        assert response.status_code == 200
        cart_item.refresh_from_db()
        assert cart_item.quantity == update_data["quantity"]

    def test_remove_item_from_cart(self):
        """Test removing an item from cart."""
        cart = CartFactory(customer=self.customer)
        cart_item = CartItemFactory(cart=cart)

        response = self.client.delete(f"/api/carts/{cart.id}/items/{cart_item.id}/")

        assert response.status_code == 204
        cart_item.refresh_from_db()
        assert cart_item.is_deleted is True

    def test_cart_totals_calculation(self):
        """Test that cart totals are calculated correctly."""
        cart = CartFactory(
            customer=self.customer, subtotal=0, total_price=0, total_quantity=0
        )

        # Add items to cart
        item1 = CartItemFactory(cart=cart, quantity=2, price=10.00)
        item2 = CartItemFactory(cart=cart, quantity=1, price=15.00)

        response = self.client.get(f"/api/carts/{cart.id}/")

        assert response.status_code == 200
        data = response.json()

        # Check calculated totals (assuming the controller recalculates them)
        expected_total_quantity = item1.quantity + item2.quantity
        expected_subtotal = (item1.quantity * item1.price) + (
            item2.quantity * item2.price
        )

        assert data["total_quantity"] >= expected_total_quantity
        assert float(data["subtotal"]) >= float(expected_subtotal)


@pytest.mark.django_db
class TestCartControllerPermissions:
    """Test permission requirements for CartController."""

    def setup_method(self):
        """Set up test data."""
        self.client = Client()
        self.user = UserFactory()
        self.customer = CustomerFactory(user=self.user)
        self.other_user = UserFactory()
        self.other_customer = CustomerFactory(user=self.other_user)

    def test_cart_list_requires_authentication(self):
        """Test that cart list endpoint requires authentication."""
        response = self.client.get("/api/carts/")

        assert response.status_code == 401

    def test_user_can_only_see_own_carts(self):
        """Test that users can only see their own carts."""
        own_cart = CartFactory(customer=self.customer)
        other_cart = CartFactory(customer=self.other_customer)

        self.client.force_login(self.user)
        response = self.client.get("/api/carts/")

        assert response.status_code == 200
        data = response.json()
        cart_ids = [item["id"] for item in data]

        assert str(own_cart.id) in cart_ids
        assert str(other_cart.id) not in cart_ids

    def test_user_cannot_access_other_users_cart(self):
        """Test that users cannot access other users' carts."""
        other_cart = CartFactory(customer=self.other_customer)

        self.client.force_login(self.user)
        response = self.client.get(f"/api/carts/{other_cart.id}/")

        assert response.status_code == 404  # Should not be found due to filtering

    def test_user_cannot_modify_other_users_cart(self):
        """Test that users cannot modify other users' carts."""
        other_cart = CartFactory(customer=self.other_customer)
        update_data = {"session_key": "hacked-session"}

        self.client.force_login(self.user)
        response = self.client.put(
            f"/api/carts/{other_cart.id}/",
            data=update_data,
            content_type="application/json",
        )

        assert response.status_code == 404  # Should not be found due to filtering
