import pytest
from django.urls import reverse
from rest_framework import status

from core.apps.articles.models import Article
from core.apps.articles.serializers import ArticlePreviewSerializer

pytestmark = pytest.mark.django_db

ARTICLE_COUNT = 21


@pytest.fixture
def existing_articles(article_factory):
    article_factory.create_batch(size=ARTICLE_COUNT)


class TestArticleListEndpoint:
    endpoint = reverse("article_list_create")

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
        articles = Article.statistic_objects.preview_data()[:10]

        # Act
        response = authenticated_client.get(self.endpoint)

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == article_count

        serializer = ArticlePreviewSerializer(articles, many=True)
        assert response.data["results"] == serializer.data

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

            articles = Article.statistic_objects.preview_data().order_by(query)
            serializer = ArticlePreviewSerializer(articles, many=True)
            assert response.data["results"] == serializer.data
