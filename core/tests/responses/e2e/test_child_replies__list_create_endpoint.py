import pytest
from django.urls import reverse
from rest_framework import status

from core.apps.responses.serializers import ResponseSerializer

pytestmark = pytest.mark.django_db


def get_endpoint(response_id):
    return reverse("next_child_replies_list_create", args=[response_id])


class TestChildRepliesListEndpoint:
    # test unauth
    def test_unauthed_get_401(self, client, response):
        endpoint = get_endpoint(response.id)
        resp = client.get(endpoint)

        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_authed_get_200_and_data_correct(
        self, authenticated_client, response_factory
    ):
        children_count = 3
        response = response_factory(with_children=children_count)
        children = response.children.all().order_by(
            "-claps_count", "-created_at", "-updated_at"
        )

        endpoint = get_endpoint(response.id)
        resp = authenticated_client.get(endpoint)

        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["count"] == children_count

        serializer = ResponseSerializer(children, many=True)
        assert resp.data["results"] == serializer.data


class TestChildRepliesCreateEndpoint:
    # Test unauth get 401
    def test_unauthed_get_401(self, client, response):
        reply_data = {"content": "test"}

        endpoint = get_endpoint(response.id)
        resp = client.post(endpoint, data=reply_data)

        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    # Test authed get 201
    def test_authed_get_201(self, authenticated_client, response):
        reply_data = {"content": "test"}

        endpoint = get_endpoint(response.id)

        resp = authenticated_client.post(endpoint, data=reply_data)

        assert resp.status_code == status.HTTP_201_CREATED
        assert resp.data["content"] == reply_data["content"]
        assert resp.data["parent_id"] == response.id
