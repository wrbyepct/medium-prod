from uuid import uuid4

import pytest
from django.urls import reverse
from rest_framework import status

from core.apps.responses.models import Response
from core.apps.responses.serializers import ResponseSerializer

pytestmark = pytest.mark.django_db


def get_endpoint(article_id):
    return reverse("top_level_response_list_create", args=[article_id])


@pytest.fixture
def assert_query_order_correct(article, authenticated_client):
    def _func(query: str):
        # Make request with query
        params = {"ordering": query}
        endpoint = get_endpoint(article.id)
        resp = authenticated_client.get(endpoint, data=params)
        assert resp.status_code == status.HTTP_200_OK

        # Assert result is equal to manually ordered data
        responses = Response.objects.filter(article=article).order_by(query)
        for result, response in zip(resp.data["results"], responses):
            assert result["id"] == str(response.id)

    return _func


class TestResponseListEndpoint:
    def test_response_endpoint__unauth_access_get_401(self, client):
        endpoint = get_endpoint(uuid4())
        resp = client.get(endpoint)

        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_response_endpoint__auth_access_successful(
        self, authenticated_client, response_factory, article
    ):
        # Arrange
        total_responses = 3
        response_factory.create_batch(size=total_responses, article=article)

        # Act
        endpoint = get_endpoint(article.id)
        resp = authenticated_client.get(endpoint)
        assert resp.status_code == status.HTTP_200_OK

        # Acssert
        # Prepare serilaizer
        responses = Response.objects.filter(article=article).order_by(
            "-claps_count", "-replies_count", "-created_at", "-updated_at"
        )
        serializer = ResponseSerializer(responses, many=True)
        assert resp.data["count"] == total_responses
        assert resp.data["results"] == serializer.data

    def test_response_endpoint__with_allowed_ordering_query_result_resp_correct(
        self,
        response_factory,
        article,
        assert_query_order_correct,
    ):
        # Arrange

        response_factory.create(with_children=1, article=article)
        response_factory.create(with_claps=1, with_children=2, article=article)
        response_factory.create(with_claps=2, article=article)

        params = [
            "claps_count",
            "-claps_count",
            "replies_count",
            "-replies_count",
            "created_at",
            "-created_at",
        ]

        for query in params:
            assert_query_order_correct(query=query)

    def test_response_endpoint__with_invalid_ordering_query_result_resp_no_effect(
        self,
        article,
        response_factory,
        authenticated_client,
    ):
        # Arrange: prepare resposnes
        contents = ["BBB", "CCC", "AAA"]
        for content in contents:
            response_factory.create(article=article, content=content)

        # Arrange: get the first instance ordered by desc content
        query = "-content"
        response = Response.objects.all().order_by(query).first()
        assert response.content == "CCC"

        # Act: Rest desc list of content
        endpoint = get_endpoint(article_id=article.id)
        param = {"ordering": query}
        resp = authenticated_client.get(endpoint, data=param)

        # Assert: request ok but no effect
        assert resp.status_code == status.HTTP_200_OK
        # Default is -created as result, the first should be "BBB" instance
        assert resp.data["results"][0]["id"] != response.id
