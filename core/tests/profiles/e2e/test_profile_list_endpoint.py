import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from pytest_bdd import given, parsers, scenarios, then, when
from rest_framework import status

from core.apps.profiles.models import Profile
from core.apps.profiles.paginations import ProfilePagination
from core.apps.profiles.serializers import ProfileSerializer

pytestmark = pytest.mark.django_db

User = get_user_model()


scenarios("./features/profile__list.feature")

# TODO: Refactor to see how to make 21 profiles available

NUM_OF_PROFILES = 21


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
    return profile_factory.create_batch(size=size)


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
    num = min(num_of_result, paginator.page_size)
    profiles = Profile.objects.all()[:num]
    serializer = ProfileSerializer(profiles, many=True)

    assert response.data["count"] == num_of_result
    assert response.data["results"] == serializer.data


"""
    Scenario: Hit all_profiles endpoint max page size correct
        Given here are 21 profiles in databases
        When an authenticated client hit all_profiles endpoint with <page_size>
        Then response status code is 200 ok
        * response data contains the <expected> number of results
        Examples:
            | page_size | expected|
            | 7  |  7 |
            | 12 | 12 |
            | 21 | 20 |

"""


@given("there are 21 profiles in databases")
def _(profile_factory):
    profile_factory.create_batch(size=NUM_OF_PROFILES)


@when(
    parsers.parse(
        "an authenticated client hit all_profiles endpoint with {page_size:d}"
    ),
    target_fixture="response",
)
def _(authenticated_client, paginator, all_profile_url, page_size):
    params = {paginator.page_size_query_param: page_size}
    return authenticated_client.get(all_profile_url, data=params)


@then(parsers.parse("response data contains the {expected:d} number of results"))
def _(response, expected):
    assert len(response.data["results"]) == expected


"""

Scenario: Hit all_profiles endpoint page links work correctly
    Given there are 21 profiles in databases
    * number of pages derived from <page_size_num>
    When an authenticated client hit all_profiles endpoint with <page_size>
    Then response status code is 200 ok
    * response next page link works correctly
    Examples:
        | page_size_num |
        | 0  |
        | 5 |
        | 21 |

"""


@given(
    parsers.parse("number of pages derived from {page_size_num:d}"),
    target_fixture="num_of_pages",
)
def _(page_size_num, paginator):
    from math import floor

    default_page_size = paginator.page_size
    max_page_size = paginator.max_page_size

    page_size = (
        min(int(max_page_size), int(page_size_num))
        if page_size_num
        else default_page_size
    )
    return floor(NUM_OF_PROFILES / page_size)


def zero_2_empty(value):
    return value if value else ""


@when(
    parsers.parse(
        "an authenticated client hit all_profiles endpoint with {page_size_num:d}"
    ),
    target_fixture="response",
    converters={"start": zero_2_empty},
)
def _(authenticated_client, paginator, page_size_num, all_profile_url):
    data = {paginator.page_size_query_param: page_size_num}
    return authenticated_client.get(all_profile_url, data=data)


@then("response next page link works correctly")
def _(authenticated_client, response, num_of_pages):
    # Simulate clicking through each next page
    for _ in range(num_of_pages):
        assert response.status_code == status.HTTP_200_OK, response.data
        assert response.data["next"] is not None, response.data["next"]
        url = response.data["next"]
        response = authenticated_client.get(url)

    assert response.data["next"] is None  # final page
