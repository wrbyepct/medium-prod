import pytest
from django.urls import reverse
from django_mock_queries.mocks import MockSet
from rest_framework import status

from core.apps.bookmarks.paginations import BookmarkPagination
from core.tests.utils.misc import get_remaining_pages

TOTAL_BOOKMARKS = 31

pytestmark = pytest.mark.django_db


def get_endpoint(slug):
    return reverse("bookmarks_list", args=[slug])


@pytest.fixture
def assert_paginated_correct(authenticated_client):
    def _assert(
        resp,
        query_num,
        paginator=BookmarkPagination,
        total_count=TOTAL_BOOKMARKS,
    ):
        """Make sure remaining pages is correct by running through the pages."""
        remaining_pages = get_remaining_pages(
            query_num,
            paginator,
            total_count,
        )

        for _ in range(remaining_pages):
            assert resp.data["next"] is not None

            endpoint = resp.data["next"]
            resp = authenticated_client.get(endpoint)
            assert resp.status_code == status.HTTP_200_OK

        assert resp.data["next"] is None

    return _assert


@pytest.mark.bbb
def test_bookmark_list_view__pagination_correct(
    self,
    authenticated_client,
    article_factory,
    mocker,
    assert_paginated_correct,
):
    """
    Test response result has correct amount with user's query.

    And remaining pages is paginated correctly
    """
    # Arrange: givne 31 bookmark
    articles = article_factory.build_batch(size=TOTAL_BOOKMARKS)

    # Arrange: prepare mock return bookmarks for get_queryset
    mocker.patch(
        "core.apps.bookmarks.views.BookmarkListView.get_queryset",
        return_value=MockSet(*articles),
    )

    # Arrange: prepare query
    default_page_size = BookmarkPagination.page_size
    max_page_size = BookmarkPagination.max_page_size
    page_query = BookmarkPagination.page_size_query_param
    page_query_params = [
        ("", default_page_size),  # query num, expected num
        (5, 5),
        (31, max_page_size),
    ]

    for query_num, expected in page_query_params:
        query = {page_query: query_num}

        # Act
        endpoint = get_endpoint("stub_slug")
        resp = authenticated_client.get(endpoint, data=query)
        assert resp.status_code == status.HTTP_200_OK
        assert len(resp.data["results"]) == expected

        # Assert
        assert_paginated_correct(resp=resp, query_num=query_num)
