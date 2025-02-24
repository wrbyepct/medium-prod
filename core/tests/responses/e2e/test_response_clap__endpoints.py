from uuid import uuid4

import pytest
from django.urls import reverse
from rest_framework import status

from core.apps.responses.exceptions import CannotRepeatClap
from core.apps.responses.models import ResponseClap

pytestmark = pytest.mark.django_db


def get_endpoint(response_id):
    return reverse("response_clap_create_destroy", args=[response_id])


class TestResponseClapCreateEndpoint:
    # unauth
    def test_unauthed_get_401(self, client):
        stub_id = uuid4()
        endpoint = get_endpoint(stub_id)
        resp = client.post(endpoint)

        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    # create clap authed & data correct 201
    def test_authed_get_201(self, response, authenticated_client, normal_user):
        endpoint = get_endpoint(response.id)

        resp = authenticated_client.post(endpoint)

        assert resp.status_code == status.HTTP_201_CREATED
        assert (
            resp.data["message"] == f"Successfully clapped the response: {response.id}"
        )
        assert ResponseClap.objects.filter(user=normal_user, response=response).exists()

    # repeating clap 400
    def test_repeating_clap_get_400(
        self, authenticated_client, normal_user, response, response_clap_factory
    ):
        # Arrange: existing clapped resposne
        response_clap_factory.create(user=normal_user, response=response)

        # Act: clap again
        endpoint = get_endpoint(response.id)
        resp = authenticated_client.post(endpoint)

        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assert resp.data["detail"] == CannotRepeatClap.default_detail

    # non-existing 404

    def test_clap_non_existing_response_get_404(self, authenticated_client, response):
        endpoint = get_endpoint(uuid4())

        resp = authenticated_client.post(endpoint)

        assert resp.status_code == status.HTTP_404_NOT_FOUND


class TestResponseClapDestroyEndpoint:
    # unauths
    def test_unauthed_get_401(self, client, response):
        endpoint = get_endpoint(response.id)

        resp = client.delete(endpoint)

        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    # auth & data correct 200
    def test_authed_get_200(
        self,
        authenticated_client,
        normal_user,
        response,
        response_clap_factory,
    ):
        # Arrange: Given a repsonse clapped by the normal  user
        response_clap_factory.create(user=normal_user, response=response)

        # Act delete it
        endpoint = get_endpoint(response.id)
        resp = authenticated_client.delete(endpoint)

        assert resp.status_code == status.HTTP_200_OK

    # non-existing 404
    def test_delete_non_existing_clap_get_404(
        self, authenticated_client, normal_user, response_clap_factory
    ):
        # Arrange: given a resposne clapped by the normal user
        response_clap_factory.create(user=normal_user)

        # Act: try to delete a clap from a non-existing resposne

        endpoint = get_endpoint(uuid4())
        resp = authenticated_client.delete(endpoint)

        assert resp.status_code == status.HTTP_404_NOT_FOUND

    # delete not own 403
    def test_delet_not_own_clap_get_404(
        self, authenticated_client, response, response_clap_factory
    ):
        response_clap_factory.create(response=response)

        endpoint = get_endpoint(response.id)
        resp = authenticated_client.delete(endpoint)

        assert resp.status_code == status.HTTP_404_NOT_FOUND
