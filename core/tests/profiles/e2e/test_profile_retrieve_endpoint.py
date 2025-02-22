import pytest
from django.urls import reverse
from rest_framework import status

from core.apps.profiles.serializers import ProfileSerializer

pytestmark = [
    pytest.mark.django_db,
    pytest.mark.e2e,
    pytest.mark.profile(type="retrieve_endpoint"),
]


class TestProfileRetrieveEndpoint:
    endpoint = reverse("me")

    def test_unauthed_get_401(self, client):
        resp = client.get(self.endpoint)

        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_authed_get_200_and_data_correct(
        self, authenticated_client, normal_user, create_profile_for_normal_user
    ):
        resp = authenticated_client.get(self.endpoint)

        profile = normal_user.profile
        serializer = ProfileSerializer(profile)

        assert resp.status_code == status.HTTP_200_OK
        assert resp.data == serializer.data
