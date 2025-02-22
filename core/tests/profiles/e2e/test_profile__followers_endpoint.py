import pytest
from django.urls import reverse
from rest_framework import status

from core.apps.profiles.serializers import FollowingSerializer

pytestmark = [
    pytest.mark.django_db,
    pytest.mark.e2e,
    pytest.mark.profile,
]


@pytest.mark.profile(type="followers_endpoint")
class TestProfileFollowersEndpoint:
    def test_unauthed_get_401(self, client, profile):
        endpoint = reverse("user_followers", args=[profile.id])

        resp = client.get(endpoint)

        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_authed_get_200_and_data_correct(
        self, authenticated_client, profile_factory
    ):
        profile = profile_factory.create(with_followers=3)

        # Act
        endpoint = reverse("user_followers", args=[profile.id])
        resp = authenticated_client.get(endpoint)

        # Arrange
        assert resp.status_code == status.HTTP_200_OK
        serializer = FollowingSerializer(profile.followers.all(), many=True)

        assert resp.data["results"] == serializer.data


@pytest.mark.profile(type="following_endpoint")
class TestProfileFollowingEndpoint:
    def test_unauthed_get_401(self, client, profile):
        endpoint = reverse("user_following", args=[profile.id])

        resp = client.get(endpoint)

        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_authed_get_200_and_data_correct(
        self, authenticated_client, profile_factory
    ):
        profile = profile_factory.create(with_following=3)

        # Act
        endpoint = reverse("user_following", args=[profile.id])
        resp = authenticated_client.get(endpoint)

        # Arrange
        assert resp.status_code == status.HTTP_200_OK
        serializer = FollowingSerializer(profile.following.all(), many=True)

        assert resp.data["results"] == serializer.data
