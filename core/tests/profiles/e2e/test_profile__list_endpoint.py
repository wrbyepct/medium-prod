import pytest
from django.urls import reverse
from pytest_bdd import given, parsers, scenarios, then
from rest_framework import status

from core.apps.profiles.models import Profile
from core.apps.profiles.paginations import ProfilePagination
from core.apps.profiles.serializers import ProfileSerializer

pytestmark = pytest.mark.django_db

scenarios("./features/profile__list.feature")

# TODO: Refactor to see how to make 21 profiles available


@pytest.fixture
def all_profile_url():
    return reverse("all_profiles")


@pytest.fixture
def paginator():
    return ProfilePagination()


"""
    Scenario: Hit all_profiles endpoint unauthed should fail
        Given an unauthed client hitting 'all_profiles' endpoint
        Then I should get 401 unauthorized
"""


@given("an unauthed client hitting 'all_profiles' endpoint", target_fixture="response")
def _(client, all_profile_url):
    return client.get(all_profile_url)


@then("I should get 401 unauthorized")
def _(response):
    return response.status_code == status.HTTP_401_UNAUTHORIZED


"""
    Scenario: Hit all_profiles endpoint authed success
        Given there are <num> profiles in databases
        * an authenticated client hit all_profiles endpoint without params
        Then response status code is 200 ok
        * response data contains the first 10 profile results
"""


@given(parsers.parse("there are {size:d} profiles in databases"))
def _(profile_factory, size):
    profile_factory.create_batch(size=size)


@given(
    "an authenticated client hit all_profiles endpoint without params",
    target_fixture="response",
)
def _(authenticated_client, all_profile_url):
    return authenticated_client.get(all_profile_url)


@then("response status code is 200 ok")
def _(response):
    assert response.status_code == status.HTTP_200_OK


@then(parsers.parse("response data contains the {num_of_result:d} profiles result"))
def _(response, num_of_result, paginator):
    num = min(
        num_of_result, paginator.page_size
    )  # cannot be more than default results per page
    profiles = Profile.objects.all()[:num]
    serializer = ProfileSerializer(profiles, many=True)

    assert response.data["count"] == num_of_result
    assert response.data["results"] == serializer.data
