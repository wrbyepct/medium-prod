import pytest
from django.urls import reverse
from rest_framework import status

pytestmark = [
    pytest.mark.django_db,
    pytest.mark.e2e,
    pytest.mark.profile(type="update_endpoint"),
]


@pytest.fixture
def update_data(mock_image_upload):
    return {
        "country": "US",
        "twitter_handle": "@test_123",
        "phone_number": "+1-418-543-8090",
        "about_me": "I'm American",
        "profile_photo": mock_image_upload,
    }


class TestProfileUpdateEndpoint:
    endpoint = reverse("me_update_profile")

    def test_unathed_get_401(self, client):
        resp = client.get(self.endpoint)

        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_authed_update_get_200_and_data_correct(
        self,
        authenticated_client,
        normal_user,
        create_profile_for_normal_user,
        update_data,
    ):
        resp = authenticated_client.patch(self.endpoint, data=update_data)

        assert resp.status_code == status.HTTP_200_OK

        profile = normal_user.profile

        assert resp.data["country"] == profile.country
        assert resp.data["twitter_handle"] == profile.twitter_handle
        assert resp.data["phone_number"] == profile.phone_number
        assert resp.data["about_me"] == profile.about_me
        assert resp.data["profile_photo"] == profile.profile_photo.url

    def test_update_invalid_fields_has_no_effect(
        self,
        normal_user,
        create_profile_for_normal_user,
        authenticated_client,
    ):
        invalid_data = {
            "first_name": "YO",
            "last_name": "MAN",
            "email": "yoman@example.com",
            "password": "testestestest123",
        }

        resp = authenticated_client.patch(self.endpoint, data=invalid_data)

        normal_user.refresh_from_db()

        assert resp.status_code == status.HTTP_200_OK

        assert normal_user.first_name != invalid_data["first_name"]
        assert normal_user.last_name != invalid_data["last_name"]
        assert normal_user.email != invalid_data["email"]
        assert not normal_user.check_password(invalid_data["password"])
