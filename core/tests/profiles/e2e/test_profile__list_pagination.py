import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from pytest_bdd import given, parsers, scenario, then, when
from rest_framework import status

from core.apps.profiles.paginations import ProfilePagination
from core.tests.profiles.fixtures.factories import ProfileFactory
from core.tests.utils.misc import get_remaining_pages

User = get_user_model()

NUM_OF_PROFILES = 21


pytestmark = pytest.mark.django_db


@pytest.fixture
def all_profile_url():
    return reverse("all_profiles")


@pytest.fixture
def paginator():
    return ProfilePagination()


@pytest.fixture
def profiles():
    ProfileFactory.create_batch(size=NUM_OF_PROFILES)


"""
    Scenario: Hit all_profiles endpoint max page size correct
        Given an authenticated client hit all_profiles endpoint with <page_size>
        Then response status code is 200 ok
        * response data contains the <expected> number of results
        Examples:
            | page_size | expected|
            | 7  |  7 |
            | 12 | 12 |
            | 21 | 20 | 
"""


@pytest.mark.aaa
@scenario(
    "./features/profile__list_pagination.feature",
    "Hit all_profiles endpoint max page size correct",
)
def test_hit_all_profiles_endpoint_max_page_size_correct(profiles):
    pass


@given(
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


@then("response status code is 200 ok")
def _(response):
    assert response.status_code == status.HTTP_200_OK


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


@pytest.mark.aaa
@scenario(
    "./features/profile__list_pagination.feature",
    "Hit all_profiles endpoint page links work correctly",
)
def test_hit_all_profiles_endpoint_page_links_work_correctly(profiles):
    pass


@given(
    parsers.parse("number of pages derived from {page_size_num:d}"),
    target_fixture="num_of_pages",
)
def _(page_size_num, paginator):
    return get_remaining_pages(
        query_size=page_size_num,
        paginator=paginator,
        total_count=NUM_OF_PROFILES,
    )


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
