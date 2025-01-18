# ruff: noqa: F403

import pytest
from faker import Faker
from pytest_factoryboy import register
from rest_framework.test import APIClient

from .factories import UserFactory

register(UserFactory)
pytestmark = pytest.mark.django_db

TEST_USER_EMAIL = "test@example.com"
TEST_USER_FIRST_NAME = "Test"
TEST_USER_LAST_NAME = "Bomb"
TEST_USER_PASSWORD = "testpassword"  # noqa: S105

fake = Faker()


@pytest.fixture
def user_data():
    return {
        "email": fake.email(),
        "first_name": TEST_USER_FIRST_NAME,
        "last_name": TEST_USER_LAST_NAME,
        "password1": TEST_USER_PASSWORD,
        "password2": TEST_USER_PASSWORD,
    }


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
