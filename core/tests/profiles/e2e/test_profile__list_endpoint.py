import pytest
from django.urls import reverse
from rest_framework import status

from core.apps.profiles.models import Profile
from core.apps.profiles.serializers import ProfileSerializer

pytestmark = [
    pytest.mark.django_db,
    pytest.mark.e2e,
    pytest.mark.profile(type="list_endpoint"),
]


class TestProfileListEndpoint:
    endpoint = reverse("all_profiles")

    def test_unauthed_get_401(self, client):
        resp = client.get(self.endpoint)

        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_authed_get_200_and_data_correct(
        self,
        authenticated_client,
        profile_factory,
    ):
        # Arrange: given 5 profiels
        profile_num = 5
        profile_factory.create_batch(size=profile_num)

        resp = authenticated_client.get(self.endpoint)

        assert resp.status_code == status.HTTP_200_OK
        assert len(resp.data["results"]) == profile_num

        profiles = Profile.objects.all().join_user_table()
        serializer = ProfileSerializer(profiles, many=True)
        assert resp.data["results"] == serializer.data
