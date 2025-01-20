import pytest
from rest_framework.serializers import ValidationError

pytestmark = pytest.mark.django_db


def test_user_behavior__create_superuser_with_is_staff_false_raise_error(user_factory):
    with pytest.raises(ValueError) as err:
        user_factory.create(is_superuser=True, is_staff=False)

    assert str(err.value) == "Superuser field: 'is_staff' must be set True."


def test_user_behavior__create_superuser_with_is_superuser_false_raise_error(
    user_factory,
):
    with pytest.raises(ValueError) as err:
        user_factory.create(is_superuser=False, is_staff=True)

    assert str(err.value) == "Superuser field: 'is_superuser' must be set True."


@pytest.mark.parametrize(
    "user_info",
    [
        {
            "email": "",  # Missing email
        },
        {
            "first_name": "",  # Missing first name
        },
        {
            "last_name": "",  # Missing last name
        },
        {
            "password": "",  # Missing password
        },
    ],
)
def test_user_model_behavior__create_regular_user_missing_fields_should_raise_value_error(
    user_info, user_factory
):
    with pytest.raises(ValueError):
        user_factory(**user_info)


@pytest.mark.parametrize(
    "user_info",
    [
        {
            "email": "",  # Missing email
        },
        {
            "first_name": "",  # Missing first name
        },
        {
            "last_name": "",  # Missing last name
        },
        {
            "password": "",  # Missing password
        },
    ],
)
def test_user_model_behavior__create_super_user_missing_fields_should_raise_value_error(
    user_info, user_factory
):
    with pytest.raises(ValueError):
        user_factory(is_superuser=True, is_staff=True, **user_info)


@pytest.mark.parametrize(
    "invalid_mail",
    [
        "plainaddress",  # Missing @ and domain
        "@missinglocal.com",  # Missing local part
        "missing@domain",  # Incomplete domain
        "missing.domain@",  # Missing domain
        "two@@domain.com",  # Multiple @ symbols
        ".invalid@email.com",  # Leading dot in local part
        "invalid@email.com.",  # Trailing dot in domain
        "invalid.@email.com",  # Trailing dot in local part
        # Length Errors
        "email@" + "d" * 256 + ".com",  # Domain > 255 chars
        # Character Errors
        "invalid<>@email.com",  # Invalid special chars
        "invalid()@email.com",  # Invalid parentheses
        "invalid[]@email.com",  # Invalid brackets
        "invalid\\@email.com",  # Invalid backslash
        "invalid,@email.com",  # Invalid comma
        "çõñτªçτ@domain.com",  # Non-ASCII chars
        # Domain Errors
        "email@-domain.com",  # Domain starts with hyphen
        "email@domain-.com",  # Domain ends with hyphen
        "email@domain.c",  # Single char TLD
        "email@domain..com",  # Multiple dots in domain
        "email@.domain.com",  # Leading dot in domain
        # Space Errors
        "invalid email@email.com",  # Space in local part
        "invalid@email com",  # Space in domain
        # RFC 5321 Errors
        "email@domain.com@domain.com",  # Multiple @ in path
        "email@domain@domain.com",  # Multiple @ symbols
        "email@[IPv6:2001:db8::1]",  # IPv6 format
    ],
)
def test_user_model_behavior__invalid_email_should_fail(invalid_mail, user_factory):
    with pytest.raises(ValidationError) as err:
        user_factory.create(email=invalid_mail)

    error_message = err.value.detail[0]
    assert (
        error_message
        == f"Email provied: {invalid_mail.lower()} is invalid. Please provide a valid email."
    )
