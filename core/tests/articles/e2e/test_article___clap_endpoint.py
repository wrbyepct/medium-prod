from uuid import uuid4

import pytest
from django.urls import reverse
from rest_framework import status

from core.apps.articles.models import Clap

pytestmark = pytest.mark.django_db


def get_endpoint(article_id):
    return reverse("clap_create_destroy", args=[article_id])


class TestArticleClapEndpoint:
    def test_article_clap__unathed_get_401(self, client, article):
        endpoint = get_endpoint(article.id)

        # Act
        response = client.post(endpoint)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_article_clap__clap_article_first_time_successful(
        self, authenticated_client, normal_user, article
    ):
        endpoint = get_endpoint(article.id)

        # Act
        response = authenticated_client.post(endpoint)

        assert response.status_code == status.HTTP_201_CREATED
        assert (
            response.data["message"]
            == f"Successfully clapped the article: {article.title}"
        )
        assert Clap.objects.filter(user=normal_user, article=article).exists()

    def test_article_clap__clap_article_second_time_get_400(
        self,
        authenticated_client,
        normal_user,
        article,
        article_clap_factory,
    ):
        # Given article been clapped by normal user
        article_clap_factory.create(user=normal_user, article=article)
        endpoint = get_endpoint(article.id)

        # Act
        response = authenticated_client.post(endpoint)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_article_clap__delete_own_clap_succesful(
        self,
        authenticated_client,
        normal_user,
        article,
        article_clap_factory,
    ):
        # Givne an own clap
        article_clap_factory.create(user=normal_user, article=article)
        endpoint = get_endpoint(article.id)

        # Act
        response = authenticated_client.delete(endpoint)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["message"] == "Successfully unclap the article."
        assert not Clap.objects.filter(user=normal_user, article=article).exists()

    def test_article_clap__delete_not_own_clap_get_404(
        self,
        authenticated_client,
        article,
        article_clap_factory,
    ):
        article_clap_factory.create(article=article)
        endpoint = get_endpoint(article.id)

        # Act
        response = authenticated_client.delete(endpoint)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert Clap.objects.count() == 1

    def test_article_clap__delete_clap_by_providing_non_existing_article_id_get_404(
        self,
        authenticated_client,
        article_clap_factory,
    ):
        article_clap_factory.create()

        endpoint = get_endpoint(uuid4())
        resposne = authenticated_client.delete(endpoint)

        assert resposne.status_code == status.HTTP_404_NOT_FOUND
        assert Clap.objects.count() == 1
