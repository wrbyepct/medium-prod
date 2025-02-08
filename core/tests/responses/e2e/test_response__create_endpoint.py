from uuid import uuid4

import pytest
from django.urls import reverse
from rest_framework import status

pytestmark = pytest.mark.django_db


def get_endpoint(article_id):
    return reverse("top_level_response_list_create", args=[article_id])


@pytest.mark.abc
class TestResponseCreateEndpoint:
    # Test unauth fail
    def test_response_create_endpoint__unauthed_get_401(self, client, article):
        response_data = {"content": "test"}
        endpoint = get_endpoint(article.id)
        resp = client.post(endpoint, data=response_data)
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    # Test create succeed
    def test_response_create_endpont__authed_get_201_and_data_correct(
        self, authenticated_client, normal_user, article
    ):
        response_data = {"content": "test"}

        endpoint = get_endpoint(article.id)
        resp = authenticated_client.post(endpoint, data=response_data)

        article.refresh_from_db()
        response = article.responses.filter(user=normal_user).first()

        assert resp.status_code == status.HTTP_201_CREATED
        assert resp.data["content"] == response.content
        assert resp.data["user_full_name"] == response.user.full_name
        assert resp.data["article"] == response.article.pkid

    # Test create with invlaid data
    @pytest.mark.parametrize("invalid_content", ["", "      "])
    def test_response_create_endpont__create_with_empty_content_get_400(
        self, article, invalid_content, authenticated_client
    ):
        response_data = {"content": invalid_content}
        endpoint = get_endpoint(article.id)

        resp = authenticated_client.post(endpoint, data=response_data)

        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    # Test create but cannot find article

    def test_response_create_endpont__create_on_non_existing_article_get_404(
        self, authenticated_client
    ):
        response_data = {"content": "test data"}

        endpoint = get_endpoint(uuid4())
        resp = authenticated_client.post(endpoint, data=response_data)

        assert resp.status_code == status.HTTP_404_NOT_FOUND
