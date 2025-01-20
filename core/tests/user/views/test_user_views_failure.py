import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


def test_user_view__retrieve_user_detail_unauthenticated_fail():
    client = APIClient()
    response = client.get(reverse("user_details"))

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_user_view__change_password__new_password_not_matching_with_400_response(
    authenticated_client, user_data
):
    password_info = {
        "old_password": user_data["password1"],
        "new_password1": "testpassword_new_new",
        "new_password2": "testpassword_new",
    }
    response = authenticated_client.post(reverse("rest_password_change"), password_info)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
