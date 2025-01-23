import pytest

from core.apps.profiles.serializers import UpdateProfileSerializer

pytestmark = pytest.mark.django_db


@pytest.mark.usefixtures("mock_media_dir")
class TestUpdateProfileSerializerSuccess:
    @pytest.fixture(autouse=True)
    def update_data(self, mock_image_upload):
        return {
            "gender": "M",
            "country": "GB",  # For UK
            "phone_number": "+8860911443567",
            "about_me": "Hey I'm test!",
            "profile_photo": mock_image_upload,
            "twitter_handle": "@test12345",
        }

    def test_profile_serializer__update_serialize_correct(self, update_data):
        serializer = UpdateProfileSerializer(data=update_data)
        assert serializer.is_valid(), serializer.errors

        data = serializer.validated_data
        fields = UpdateProfileSerializer.Meta.fields
        for field in fields:
            assert field in data
            assert update_data[field] == data[field]

    def test_profile_serializer__update_serializer_save_method_correct(
        self, profile, update_data
    ):
        serializer = UpdateProfileSerializer(instance=profile, data=update_data)
        assert serializer.is_valid(), serializer.errors

        serializer.save()
        profile.refresh_from_db()

        assert profile.gender == update_data["gender"]
        assert profile.country == update_data["country"]
        assert profile.phone_number == update_data["phone_number"]
        assert profile.about_me == update_data["about_me"]
        assert profile.profile_photo == update_data["profile_photo"].name
        assert profile.twitter_handle == update_data["twitter_handle"]

    def test_profile_serializer__serialize_invalid_fields_have_no_effect(self):
        invalid_data = {
            "gender": "M",
            "country": "GB",  # For UK
            "phone_number": "+8860911443567",
            "about_me": "Hey I'm test!",
            "twitter_handle": "@test12345",
            # Invalid fields below
            "id": 20,
            "first_name": "Jim",
            "last_name": "Hall",
            "full_name": "Jim Hall",
            "email": "test@example.com",
        }
        serializer = UpdateProfileSerializer(data=invalid_data)

        assert serializer.is_valid(), serializer.errors

        data = serializer.validated_data

        assert "id" not in data
        assert "first_name" not in data
        assert "last_name" not in data
        assert "full_name" not in data
        assert "email" not in data


@pytest.mark.parametrize(
    "field, value",
    [
        ("gender", "I"),
        ("country", ""),  # Empty value
        ("country", "AAA"),  # Wrong country code
        ("city", ""),  # Empty value
        ("city", 123),  # Wrong type
        ("twitter_handle", 123),  # Wrong type
        ("profile_photo", 123),  # Wrong type
        ("profile_photo", "123"),  # Wrong type
        ("phone_number", "12312"),  # Invalid number
    ],
)
def test_profile_serializer__invalid_gender_data(profile, field, value):
    invalid_data = {field: value}
    serializer = UpdateProfileSerializer(instance=profile, data=invalid_data)
    assert not serializer.is_valid()
