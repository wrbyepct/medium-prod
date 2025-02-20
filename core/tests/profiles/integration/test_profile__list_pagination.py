import pytest
from django.urls import reverse
from django_mock_queries.mocks import MockSet

from core.apps.profiles.paginations import ProfilePagination

pytestmark = pytest.mark.django_db

TOTAL_PROFILES = 21


def test_profile_list_view__pagination_correct(
    authenticated_client,
    profile_factory,
    mocker,
    assert_paginated_correct,
):
    # Arrange: queryset
    profiles = profile_factory.build_batch(size=TOTAL_PROFILES)
    mocker.patch(
        "core.apps.profiles.views.ProfileListAPIView.get_queryset",
        return_value=MockSet(*profiles),
    )

    # Arrange: queries
    default_page_size = ProfilePagination.page_size
    max_page_size = ProfilePagination.max_page_size
    page_size_query_param = ProfilePagination.page_size_query_param

    scenarios = [
        ("", default_page_size),
        (5, 5),
        (21, max_page_size),
    ]

    # Act & assert
    for query_num, expected_num in scenarios:
        endpoint = reverse("all_profiles")
        query = {page_size_query_param: query_num}
        resp = authenticated_client.get(endpoint, query)
        assert len(resp.data["results"]) == expected_num

        assert_paginated_correct(
            resp=resp,
            query_num=query_num,
            paginator=ProfilePagination,
            total_count=TOTAL_PROFILES,
        )
