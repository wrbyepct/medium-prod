import pytest
from django.urls import reverse
from rest_framework import status

from core.apps.articles.models import Article
from core.apps.articles.paginations import ArticlePagination
from core.apps.articles.serializers import ArticleSerializer
from core.tests.utils.misc import get_remaining_pages

pytestmark = pytest.mark.django_db

ARTICLE_COUNT = 21


@pytest.fixture
def existing_articles(article_factory):
    article_factory.create_batch(size=ARTICLE_COUNT)


@pytest.fixture
def article_paginator():
    return ArticlePagination()


class TestArticleListEndpoint:
    endpoint = reverse("article_list_create")
    paginator = ArticlePagination()

    # unauth denied
    def test_article_list_endpoint__unauthed_deny_access(self, client):
        response = client.get(self.endpoint)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # authed success
    def test_article_list_endpoint__authed_access_success(
        self, authenticated_client, existing_articles
    ):
        # Arrange
        article_count = Article.objects.count()
        articles = Article.statistic_objects.all()[:10]

        # Act
        response = authenticated_client.get(self.endpoint)

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == article_count

        serializer = ArticleSerializer(articles, many=True)
        assert response.data["results"] == serializer.data

    # pagination
    def test_article_list_endpoint__pagination_correct(
        self, authenticated_client, existing_articles
    ):
        # Gvien query data {"page_size": <number>} and make request
        for page_size in ["", 5, 21]:
            page_size_query_param = self.paginator.page_size_query_param
            param = {page_size_query_param: page_size}

            # and first page response 200
            response = authenticated_client.get(self.endpoint, data=param)
            assert response.status_code == status.HTTP_200_OK

            remaining_pages = get_remaining_pages(
                query_pages=page_size,
                paginator=self.paginator,
                total_count=response.data["count"],
            )

            for _ in range(remaining_pages):
                assert response.status_code == status.HTTP_200_OK
                assert response.data["next"] is not None
                next_url = response.data["next"]
                response = authenticated_client.get(next_url)

            assert response.data["next"] is None

    # ordering

    def test_article_list_view__ordering_query_correct(
        self, article_factory, authenticated_client
    ):
        # Given db has 5 articles
        article_factory.create_batch(size=5)

        for query in ["created_at", "-created_at", "title", "-title"]:
            # When request endpoint with order query
            param = {"ordering": query}
            response = authenticated_client.get(self.endpoint, data=param)

            articles = Article.statistic_objects.all().order_by(query)
            serializer = ArticleSerializer(articles, many=True)
            assert response.data["results"] == serializer.data
