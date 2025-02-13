from uuid import uuid4

import pytest
from django.urls import reverse
from rest_framework import status

from core.apps.ratings.models import Rating

pytestmark = pytest.mark.django_db


def get_endpoint(rating_id):
    return reverse("rating_update_destory", args=[rating_id])


class TestRatingUpdateEndpoint:
    # test unauth get 401
    def test_unauthed_get_401(self, client, rating):
        data = {"rating": 1, "review": "good"}

        endpoint = get_endpoint(rating.id)
        resp = client.patch(endpoint, data=data)

        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    # test authed get 200 and data correct
    def test_authed_get_200_and_data_updated_correct(
        self, authenticated_client, normal_user, rating
    ):
        data = {"rating": 1, "review": "good"}
        endpoint = get_endpoint(rating.id)
        resp = authenticated_client.patch(endpoint, data=data)

        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["user_full_name"] == normal_user.full_name
        assert resp.data["rating"] == data["rating"]
        assert resp.data["review"] == data["review"]

    # test udpate valid invalid get 400
    def test_update_with_invalid_data(self, authenticated_client, rating):
        invalid_data = {"rating": -1, "review": "good"}

        endpoint = get_endpoint(rating.id)

        resp = authenticated_client.patch(endpoint, data=invalid_data)
        rating.refresh_from_db()

        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assert rating.rating != invalid_data["rating"]
        assert rating.review != invalid_data["review"]

    # test update not own get 403
    def test_update_not_own_instnace_get_403(
        self, authenticated_client, rating_factory
    ):
        not_own_rating = rating_factory.create()

        endpoint = get_endpoint(not_own_rating.id)
        data = {"rating": 1, "review": "good"}
        resp = authenticated_client.patch(endpoint, data=data)

        assert resp.status_code == status.HTTP_403_FORBIDDEN


class TestRatingDeleteEndpoint:
    # test unauth get 401
    def test_unauth_get_401(self, client, rating):
        endpoint = get_endpoint(rating.id)

        resp = client.delete(endpoint)

        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    # test authed get 200 and instance deleted
    def test_authed_get_200_and_instance_deleted(self, rating, authenticated_client):
        endpoint = get_endpoint(rating.id)

        resp = authenticated_client.delete(endpoint)

        assert resp.status_code == status.HTTP_200_OK
        assert not Rating.objects.filter(id=rating.id).exists()

    # test delete not own get 403
    def test_delete_not_own_rating_get_403(self, rating_factory, authenticated_client):
        not_own_rating = rating_factory.create()

        endpoint = get_endpoint(not_own_rating.id)

        resp = authenticated_client.delete(endpoint)

        assert resp.status_code == status.HTTP_403_FORBIDDEN

    # test delete non-existing get 404
    def test_delete_non_existing_rating_get_404(self, authenticated_client):
        endpoint = get_endpoint(uuid4())

        resp = authenticated_client.delete(endpoint)

        assert resp.status_code == status.HTTP_404_NOT_FOUND
