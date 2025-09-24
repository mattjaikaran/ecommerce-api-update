import pytest

from .factories import AdminUserFactory, CustomerFactory, SuperUserFactory, UserFactory


@pytest.fixture
def user():
    """Create a regular user."""
    return UserFactory()


@pytest.fixture
def admin_user():
    """Create an admin user."""
    return AdminUserFactory()


@pytest.fixture
def superuser():
    """Create a superuser."""
    return SuperUserFactory()


@pytest.fixture
def customer(user):
    """Create a customer linked to a user."""
    return CustomerFactory(user=user)
