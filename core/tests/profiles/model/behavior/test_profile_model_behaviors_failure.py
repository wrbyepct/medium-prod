import pytest
from django.db import DataError

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    "invalid_phone_number, error",
    [
        ("+886095312787609531278760953127876", DataError),  # Exceeds 30 length
        (8860953127876, TypeError),  # Not string
    ],
)
def test_profile_model_behavior__phonenumber_invalid_create_fail(
    invalid_phone_number,
    error,
    profile_factory,
):
    with pytest.raises(error):
        profile_factory.create(phone_number=invalid_phone_number)


# Test gender choice not correct, exceeds max_length

# Test twittwer handle exceeds max_length

# Test country name blank string

# city name blank string
