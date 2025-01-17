import pytest
from faker import Faker

from .constants import (
    TEST_USER_FIRST_NAME,
    TEST_USER_LAST_NAME,
    TEST_USER_PASSWORD,
)

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
