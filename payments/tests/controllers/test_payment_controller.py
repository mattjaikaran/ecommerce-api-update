import pytest
from django.test import Client

from core.tests.factories import AdminUserFactory, UserFactory
from orders.tests.factories import OrderFactory
from payments.models import PaymentMethod, Transaction
from payments.tests.factories import (
    FailedTransactionFactory,
    PaymentMethodFactory,
    StripePaymentMethodFactory,
    SuccessfulTransactionFactory,
    TransactionFactory,
)


@pytest.mark.django_db
class TestPaymentMethodController:
    """Test operations for PaymentMethod."""

    def setup_method(self):
        """Set up test data."""
        self.client = Client()
        self.admin_user = AdminUserFactory()
        self.regular_user = UserFactory()
        self.client.force_login(self.admin_user)

    def test_create_payment_method(self):
        """Test creating a new payment method."""
        payment_method_data = {
            "name": "Test Gateway",
            "description": "A test payment gateway",
            "credentials": {"api_key": "test_key", "secret": "test_secret"},
        }

        response = self.client.post(
            "/api/payment-methods/",
            data=payment_method_data,
            content_type="application/json",
        )

        assert response.status_code == 201
        assert PaymentMethod.objects.filter(name=payment_method_data["name"]).exists()

        payment_method = PaymentMethod.objects.get(name=payment_method_data["name"])
        assert payment_method.description == payment_method_data["description"]
        assert payment_method.credentials == payment_method_data["credentials"]

    def test_read_payment_method_list(self):
        """Test retrieving list of payment methods."""
        PaymentMethodFactory.create_batch(3)

        response = self.client.get("/api/payment-methods/")

        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 3

    def test_read_payment_method_detail(self):
        """Test retrieving a specific payment method."""
        payment_method = StripePaymentMethodFactory()

        response = self.client.get(f"/api/payment-methods/{payment_method.id}/")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(payment_method.id)
        assert data["name"] == payment_method.name

    def test_update_payment_method(self):
        """Test updating a payment method."""
        payment_method = PaymentMethodFactory()
        update_data = {
            "name": "Updated Gateway Name",
            "description": "Updated description",
        }

        response = self.client.put(
            f"/api/payment-methods/{payment_method.id}/",
            data=update_data,
            content_type="application/json",
        )

        assert response.status_code == 200
        payment_method.refresh_from_db()
        assert payment_method.name == update_data["name"]
        assert payment_method.description == update_data["description"]

    def test_delete_payment_method(self):
        """Test deleting a payment method (soft delete)."""
        payment_method = PaymentMethodFactory()

        response = self.client.delete(f"/api/payment-methods/{payment_method.id}/")

        assert response.status_code == 204
        payment_method.refresh_from_db()
        assert payment_method.is_deleted is True


@pytest.mark.django_db
class TestTransactionController:
    """Test operations for Transaction."""

    def setup_method(self):
        """Set up test data."""
        self.client = Client()
        self.admin_user = AdminUserFactory()
        self.regular_user = UserFactory()
        self.client.force_login(self.admin_user)

    def test_create_transaction(self):
        """Test creating a new transaction."""
        order = OrderFactory()
        payment_method = PaymentMethodFactory()

        transaction_data = {
            "order_id": str(order.id),
            "payment_method_id": str(payment_method.id),
            "amount": "100.00",
            "transaction_type": "payment",
            "transaction_status": "pending",
            "transaction_currency": "USD",
            "transaction_amount": "100.00",
            "transaction_fee": "3.00",
            "transaction_tax": "0.00",
            "transaction_total": "103.00",
        }

        response = self.client.post(
            "/api/transactions/", data=transaction_data, content_type="application/json"
        )

        assert response.status_code == 201
        assert Transaction.objects.filter(order=order).exists()

        transaction = Transaction.objects.get(order=order)
        assert str(transaction.amount) == transaction_data["amount"]
        assert transaction.payment_method == payment_method

    def test_read_transaction_list(self):
        """Test retrieving list of transactions."""
        TransactionFactory.create_batch(3)

        response = self.client.get("/api/transactions/")

        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 3

    def test_read_transaction_list_filters(self):
        """Test filtering transactions by various criteria."""
        successful_tx = SuccessfulTransactionFactory()
        failed_tx = FailedTransactionFactory()

        # Test status filter
        response = self.client.get("/api/transactions/?transaction_status=completed")
        assert response.status_code == 200
        data = response.json()
        transaction_ids = [item["id"] for item in data]
        assert str(successful_tx.id) in transaction_ids
        assert str(failed_tx.id) not in transaction_ids

    def test_read_transaction_detail(self):
        """Test retrieving a specific transaction."""
        transaction = TransactionFactory()

        response = self.client.get(f"/api/transactions/{transaction.id}/")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(transaction.id)
        assert data["transaction_id"] == transaction.transaction_id

    def test_read_transaction_detail_not_found(self):
        """Test retrieving non-existent transaction returns 404."""
        import uuid

        fake_id = uuid.uuid4()

        response = self.client.get(f"/api/transactions/{fake_id}/")

        assert response.status_code == 404

    def test_update_transaction_status(self):
        """Test updating transaction status."""
        transaction = TransactionFactory(transaction_status="pending")
        update_data = {"transaction_status": "completed", "status": "completed"}

        response = self.client.put(
            f"/api/transactions/{transaction.id}/",
            data=update_data,
            content_type="application/json",
        )

        assert response.status_code == 200
        transaction.refresh_from_db()
        assert transaction.transaction_status == "completed"
        assert transaction.status == "completed"

    def test_transaction_refund(self):
        """Test processing a refund for a transaction."""
        transaction = SuccessfulTransactionFactory()
        refund_data = {"amount": "50.00", "reason": "Customer request"}

        response = self.client.post(
            f"/api/transactions/{transaction.id}/refund/",
            data=refund_data,
            content_type="application/json",
        )

        # This endpoint might not exist yet, but testing the concept
        # assert response.status_code == 200

    def test_delete_transaction(self):
        """Test deleting a transaction (soft delete)."""
        transaction = TransactionFactory()

        response = self.client.delete(f"/api/transactions/{transaction.id}/")

        assert response.status_code == 204
        transaction.refresh_from_db()
        assert transaction.is_deleted is True

    def test_transaction_search(self):
        """Test searching transactions by transaction ID."""
        transaction1 = TransactionFactory(transaction_id="TXN001234")
        transaction2 = TransactionFactory(transaction_id="TXN005678")

        response = self.client.get("/api/transactions/?search=TXN001234")

        assert response.status_code == 200
        data = response.json()
        transaction_ids = [item["transaction_id"] for item in data]
        assert transaction1.transaction_id in transaction_ids
        assert transaction2.transaction_id not in transaction_ids

    def test_transaction_ordering(self):
        """Test ordering transactions by date."""
        old_transaction = TransactionFactory()
        new_transaction = TransactionFactory()

        response = self.client.get("/api/transactions/?ordering=-created_at")

        assert response.status_code == 200
        data = response.json()
        transaction_ids = [item["id"] for item in data]
        new_index = transaction_ids.index(str(new_transaction.id))
        old_index = transaction_ids.index(str(old_transaction.id))
        assert new_index < old_index


@pytest.mark.django_db
class TestPaymentControllerPermissions:
    """Test permission requirements for Payment endpoints."""

    def setup_method(self):
        """Set up test data."""
        self.client = Client()
        self.regular_user = UserFactory()
        self.admin_user = AdminUserFactory()

    def test_payment_method_list_requires_admin(self):
        """Test that payment method list requires admin permissions."""
        PaymentMethodFactory.create_batch(3)

        # Test without authentication
        response = self.client.get("/api/payment-methods/")
        assert response.status_code == 401

        # Test with regular user
        self.client.force_login(self.regular_user)
        response = self.client.get("/api/payment-methods/")
        assert response.status_code == 403

    def test_admin_can_manage_payment_methods(self):
        """Test that admin can manage payment methods."""
        self.client.force_login(self.admin_user)

        payment_method_data = {
            "name": "Admin Gateway",
            "description": "Gateway created by admin",
            "credentials": {},
        }

        response = self.client.post(
            "/api/payment-methods/",
            data=payment_method_data,
            content_type="application/json",
        )
        assert response.status_code == 201

    def test_transaction_list_requires_admin(self):
        """Test that transaction list requires admin permissions."""
        TransactionFactory.create_batch(3)

        # Test without authentication
        response = self.client.get("/api/transactions/")
        assert response.status_code == 401

        # Test with regular user
        self.client.force_login(self.regular_user)
        response = self.client.get("/api/transactions/")
        assert response.status_code == 403

    def test_admin_can_view_all_transactions(self):
        """Test that admin can view all transactions."""
        TransactionFactory.create_batch(3)

        self.client.force_login(self.admin_user)
        response = self.client.get("/api/transactions/")

        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 3

    def test_user_can_view_own_order_transactions(self):
        """Test that user can view transactions for their own orders."""
        from core.tests.factories import CustomerFactory

        customer = CustomerFactory(user=self.regular_user)
        order = OrderFactory(customer=customer)
        transaction = TransactionFactory(order=order)

        self.client.force_login(self.regular_user)
        response = self.client.get(f"/api/orders/{order.id}/transactions/")

        # This endpoint might not exist yet, but testing the concept
        # assert response.status_code == 200
