import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from core.apps.profiles.models import Profile
from core.apps.profiles.serializers import ProfileSerializer
from core.tests.profiles.fixtures.factories import ProfileFactory
from core.tests.utils.misc import full_url

pytestmark = pytest.mark.django_db

User = get_user_model()


@pytest.fixture(scope="module")
def profiles(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        User.objects.all().delete()

        ProfileFactory.create_batch(size=21)
        yield


class TestProfileListAPIViewSuccess:
    url = reverse("all_profiles")

    def test_profile_list_view__authenticated_only(self, unauth_client):
        response = unauth_client.get(self.url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_profile_list_view__get_request_success(
        self, authenticated_client, profile_factory
    ):
        num_profiles = 5
        profile_factory.create_batch(size=num_profiles)
        profiles = (
            Profile.objects.all()
        )  # Default order is '-created_at' at the db level.

        response = authenticated_client.get(self.url)
        serializer = ProfileSerializer(profiles, many=True)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == num_profiles
        assert response.data["next"] is None
        assert response.data["previous"] is None
        assert response.data["results"] == serializer.data

    @pytest.mark.parametrize(
        "param, expected",
        [
            (None, 10),
            ({"page_size": 7}, 7),
            ({"page_size": 12}, 12),
            ({"page_size": 21}, 20),
        ],
    )
    def test_profile_list_view__pagination_page_size_correct(
        self, profiles, authenticated_client, param, expected
    ):
        response = authenticated_client.get(self.url, data=param)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == expected

    @pytest.mark.parametrize(
        "param, previous, next",
        [
            (None, None, lambda url: full_url(url=url, query_term="?page=2")),
            (
                {"page": 2},
                lambda url: full_url(url=url),
                lambda url: full_url(url=url, query_term="?page=3"),
            ),
            (
                {"page": 3},
                lambda url: full_url(url=url, query_term="?page=2"),
                None,
            ),
        ],
    )
    def test_profile_list_view__pagination_page_correct(
        self, profiles, authenticated_client, param, previous, next
    ):
        response = authenticated_client.get(self.url, data=param)

        assert response.status_code == status.HTTP_200_OK

        expected_previous = previous(self.url) if callable(previous) else previous
        expected_next = next(self.url) if callable(next) else next

        assert response.data["previous"] == expected_previous
        assert response.data["next"] == expected_next
