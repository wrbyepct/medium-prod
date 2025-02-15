import json
import time
from datetime import datetime
from uuid import uuid4

import pytest
from django.urls import reverse
from rest_framework import status

from core.apps.articles.models import Article
from core.apps.articles.serializers import ArticleSerializer

pytestmark = pytest.mark.django_db


def get_endpont(article_id):
    return reverse("article_retrieve_update_destroy", args=[article_id])


@pytest.fixture
def mock_article_es_delete(mocker):
    mocker.patch("core.apps.articles.signals.registry.delete")


@pytest.fixture
def mock_article_es_update(mocker):
    mocker.patch("core.apps.articles.signals.registry.update")


class TestArticleRetreiveEndpoint:
    def test_article_retrieve_endpoint__unauthed_should_get_401(self, client):
        endpoint = get_endpont(uuid4())
        response = client.get(endpoint)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_article_retrieve_endpoint__authed_access_successful(
        self, article, authenticated_client
    ):
        endpoint = get_endpont(article.id)

        response = authenticated_client.get(endpoint)

        assert response.status_code == status.HTTP_200_OK

        article = Article.statistic_objects.get(id=article.id)
        serializer = ArticleSerializer(article)
        assert response.data == serializer.data

    def test_article_retrieve_endpoint__get_non_existing_article_should_get_404(
        self, article, authenticated_client
    ):
        endpoint = get_endpont(uuid4())
        response = authenticated_client.get(endpoint)

        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestTestArticleDesctroyEndpoint:
    def test_article_destroy_endpoint__delete_own_article_successful(
        self, authenticated_client, article_factory, normal_user, mock_article_es_delete
    ):
        article = article_factory(author=normal_user)

        endpoint = get_endpont(article.id)
        response = authenticated_client.delete(endpoint)

        assert response.status_code == status.HTTP_200_OK
        assert not Article.objects.filter(id=article.id).exists()

    def test_article_destroy_endpoint_delete_not_own_article_get_403(
        self, authenticated_client, article
    ):
        endpoint = get_endpont(article.id)
        response = authenticated_client.delete(endpoint)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Article.objects.filter(id=article.id).exists()


class TestArticleUpdateEndpoint:
    def test_article_update_view__udpate_own_article_success(
        self,
        authenticated_client,
        normal_user,
        article_factory,
        mock_image_upload,
        mock_media_dir,
        mock_article_es_update,
    ):
        article = article_factory.create(author=normal_user)

        update_data = {
            "title": "New Title",
            "body": "New Body",
            "description": "New Description",
            "tags": '["New A", "New B", "New C"]',
            "banner_image": mock_image_upload,
        }
        endpoint = get_endpont(article.id)
        response = authenticated_client.patch(endpoint, data=update_data)

        assert response.status_code == status.HTTP_200_OK, response.data
        assert response.data["title"] == update_data["title"]
        assert response.data["body"] == update_data["body"]
        assert response.data["description"] == update_data["description"]
        assert response.data["tags"] == json.loads(update_data["tags"])

        response_image_name = response.data["banner_image"].split("/")[-1]
        assert response_image_name == update_data["banner_image"].name

    def test_article_update_view__update_not_own_article_get_403(
        self, authenticated_client, article
    ):
        endpoint = get_endpont(article.id)

        update_data = {
            "title": "New Title",
        }
        response = authenticated_client.patch(endpoint)

        assert response.status_code == status.HTTP_403_FORBIDDEN

        article.refresh_from_db()
        assert article.title != update_data["title"]

    def test_article_update_view__update_read_only_fields_no_effect(
        self,
        authenticated_client,
        normal_user,
        article_factory,
        mock_article_es_update,
    ):
        article = article_factory.create(author=normal_user)
        old_article = Article.statistic_objects.get(id=article.id)
        old_serializer = ArticleSerializer(old_article)

        update_data = {
            "estimated_reading_time": "some data",
            "avg_rating": "some data",
            "views": "some data",
            "responses_count": "some data",
            "claps_count": "some data",
            "clapped_by": "some data",
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "author_info": "some data",
        }

        # Act
        time.sleep(1)  # Explicitly wait for 1s to see update_at difference
        endpoint = get_endpont(article.id)
        response = authenticated_client.patch(endpoint, data=update_data)

        # Assert
        assert response.status_code == status.HTTP_200_OK

        new_article = Article.statistic_objects.get(id=article.id)
        new_serializer = ArticleSerializer(new_article)

        # Only updated_at will be differnt
        assert new_serializer.data["updated_at"] != old_serializer.data["updated_at"]
        # But it's not the same as the provided data
        assert new_serializer.data["updated_at"] != update_data["updated_at"]

        old_data = dict(old_serializer.data)
        new_data = dict(new_serializer.data)

        old_data.pop("updated_at")
        new_data.pop("updated_at")
        assert new_data == old_data

    def test_article_update_endpoint__provide_invalid_type_get_400(
        self,
        article_factory,
        authenticated_client,
        normal_user,
    ):
        article = article_factory.create(author=normal_user)

        endpoint = get_endpont(article.id)

        invalid_data = [
            {"title": "1" * 256},
            {"banner_image": 123},
            {"tags": ["New A", "New B", "New C"]},  # This will let only 'New C' be sent
        ]

        for data in invalid_data:
            # Act
            response = authenticated_client.patch(endpoint, data=data)

            assert response.status_code == status.HTTP_400_BAD_REQUEST

            article.refresh_from_db()
            field = next(iter(data))
            assert getattr(article, field) != data[field]
