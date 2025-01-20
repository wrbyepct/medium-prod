import pytest
from rest_framework.serializers import ValidationError

from core.apps.user.serializers import CustomRegisterSerializer, UserSerializer

pytestmark = pytest.mark.django_db


def test_user_serializer__convert_normal_user_instance_correctly(normal_user):
    serializer = UserSerializer(normal_user)

    assert "id" in serializer.data
    assert "email" in serializer.data
    assert "first_name" in serializer.data
    assert "last_name" in serializer.data
    assert "gender" in serializer.data
    assert "phone_number" in serializer.data
    assert "profile_photo" in serializer.data
    assert "country" in serializer.data
    assert "city" in serializer.data
    assert "admin" not in serializer.data


def test_user_serializer__convert_super_user_instance_correctly(super_user):
    serializer = UserSerializer(super_user)

    assert "id" in serializer.data
    assert "email" in serializer.data
    assert "first_name" in serializer.data
    assert "last_name" in serializer.data
    assert "gender" in serializer.data
    assert "phone_number" in serializer.data
    assert "profile_photo" in serializer.data
    assert "country" in serializer.data
    assert "city" in serializer.data
    assert "admin" in serializer.data
    assert serializer.data["admin"] is True


def test_user_register_serializer__save_method_return_user_instance(
    mock_create_user_side_effect, user_data, mock_request
):
    serializer = CustomRegisterSerializer(data=user_data)

    assert serializer.is_valid()

    user = serializer.save(mock_request)

    assert user.email == user_data["email"]
    assert user.first_name == user_data["first_name"]
    assert user.last_name == user_data["last_name"]
    assert user.check_password(user_data["password1"])


def test_user_register_serializer__password_not_match_raise_validation_error():
    invlaid_data = {
        "first_name": "Test",
        "last_name": "Test",
        "email": "test@example.com",
        "password1": "password12345",
        "password2": "password12345_wrong",
    }

    with pytest.raises(ValidationError):  # noqa: PT012
        serializer = CustomRegisterSerializer(data=invlaid_data)
        serializer.is_valid(raise_exception=True)


@pytest.mark.parametrize(
    "invalid_data",
    [
        {
            "first_name": "T" * 51,
            "last_name": "Test",
            "email": "test@example.com",
            "password1": "password12345",
            "password2": "password12345",
        },
        {
            "first_name": "Test",
            "last_name": "T" * 51,
            "email": "test@example.com",
            "password1": "password12345",
            "password2": "password12345",
        },
    ],
)
def test_user_register_serializer__name_exceeding_len50_raise_validation_error(
    invalid_data,
):
    with pytest.raises(ValidationError):  # noqa: PT012
        serializer = CustomRegisterSerializer(data=invalid_data)
        serializer.is_valid(raise_exception=True)
