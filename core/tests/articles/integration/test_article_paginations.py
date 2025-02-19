import pytest
from django.urls import reverse
from django_mock_queries.mocks import MockSet

from core.apps.articles.paginations import ArticlePagination

pytestmark = pytest.mark.django_db

TOTAL_ARTICLES = 21


@pytest.mark.bbb
def test_article_list_view__pagination_correct(
    authenticated_client,
    article_factory,
    mocker,
    assert_paginated_correct,
):
    # Arrange: 21 articles in memory
    articles = article_factory.build_batch(size=TOTAL_ARTICLES)

    # Arrange: prepre mock queyrset
    mocker.patch(
        "core.apps.articles.views.ArticleListCreateView.get_queryset",
        return_value=MockSet(*articles),
    )

    default_page_size = ArticlePagination.page_size
    max_page_size = ArticlePagination.max_page_size
    query_param = ArticlePagination.page_size_query_param

    scenarios = [
        ("", default_page_size),
        (12, 12),
        (max_page_size + 1, max_page_size),
    ]

    for query_num, expected_num in scenarios:
        endpoint = reverse("article_list_create")
        query = {query_param: query_num}

        resp = authenticated_client.get(endpoint, query)

        assert len(resp.data["results"]) == expected_num

        assert_paginated_correct(
            query_num=query_num,
            resp=resp,
            paginator=ArticlePagination,
            total_count=TOTAL_ARTICLES,
        )
