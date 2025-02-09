from datetime import datetime
from uuid import uuid4

import pytest
from django.urls import reverse
from rest_framework import status

pytestmark = pytest.mark.django_db


def get_endpoint(response_id):
    return reverse("response_update_destroy", args=[response_id])


class TestResponseUpdateEndpoint:
    def test_unauthed_get_401(self, client, response):
        endpoint = get_endpoint(response.id)
        resp = client.patch(endpoint)

        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_own_and_valid_fields_get_200_and_data_correct(
        self, authenticated_client, normal_user, response_factory
    ):
        response = response_factory.create(user=normal_user)

        update_data = {"content": "Test Test"}

        endpoint = get_endpoint(response.id)
        resp = authenticated_client.patch(endpoint, data=update_data)

        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["content"] == update_data["content"]

    @pytest.mark.parametrize("content", ["", "   "])
    def test_update_with_empty_content_get_400(
        self, authenticated_client, normal_user, response_factory, content
    ):
        response = response_factory.create(user=normal_user)
        update_data = {"content": content}

        endpoint = get_endpoint(response.id)
        resp = authenticated_client.patch(endpoint, data=update_data)

        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assert "Response content cannot be empty." in resp.data["content"]

    @pytest.mark.bbb
    @pytest.mark.parametrize(
        "invalid_field, data",
        [
            ("user_full_name", "Test Test"),
            ("article", 123),
            ("parent", 123),
            ("claps_count", 123),
            ("replies_count", 123),
            ("created_at", datetime.now()),
        ],
    )
    def test_update_invalid_fields_no_effect(
        self, authenticated_client, normal_user, response_factory, invalid_field, data
    ):
        response = response_factory.create(user=normal_user)
        update_data = {invalid_field: data}
        endpoint = get_endpoint(response.id)
        resp = authenticated_client.patch(endpoint, data=update_data)

        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[invalid_field] != update_data[invalid_field]


class TestResponseDestroyEndpoint:
    # unauth 401
    def test_unauthed_get_401(self, client, response):
        endpoint = get_endpoint(response.id)
        resp = client.delete(endpoint)

        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    # delete own success

    def test_authed_get_200(self, authenticated_client, normal_user, response_factory):
        response = response_factory.create(user=normal_user)

        endpoint = get_endpoint(response.id)
        resp = authenticated_client.delete(endpoint)
        assert resp.status_code == status.HTTP_200_OK

    # delete not own get 403
    def test_delete_own_get_403(self, authenticated_client, response):
        endpoint = get_endpoint(response.id)
        resp = authenticated_client.delete(endpoint)
        assert resp.status_code == status.HTTP_403_FORBIDDEN

    # delete not existing 404
    def test_delete_non_existing_get_404(self, authenticated_client, response):
        endpoint = get_endpoint(uuid4())
        resp = authenticated_client.delete(endpoint)
        assert resp.status_code == status.HTTP_404_NOT_FOUND
