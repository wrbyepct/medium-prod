import pytest
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


@pytest.fixture
def normal_user(user_factory):
    return user_factory.create()


@pytest.fixture
def super_user(user_factory):
    return user_factory.create(is_superuser=True, is_staff=True)


@pytest.fixture
def authenticated_client(normal_user):
    client = APIClient()
    client.force_authenticate(user=normal_user)
    return client
