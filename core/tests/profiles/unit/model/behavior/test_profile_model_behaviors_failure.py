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
def test_profile_model_behavior__geneder_exceeds_length(profile_factory):
    gender = "O" * 21
    with pytest.raises(DataError):
        profile_factory.create(gender=gender)


# Test twittwer handle exceeds max_length
def test_profile_model_behavior__twitter_handle_exceeds_length(profile_factory):
    twitter_handle = "O" * 21
    with pytest.raises(DataError):
        profile_factory.create(twitter_handle=twitter_handle)
