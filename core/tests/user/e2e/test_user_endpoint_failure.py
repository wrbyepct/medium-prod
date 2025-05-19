import pytest
from django.urls import reverse
from rest_framework import status

pytestmark = [
    pytest.mark.django_db,
    pytest.mark.e2e,
    pytest.mark.user(type="detail_endpoint"),
]


def test_user_endpoint__retrieve_user_detail_unauthenticated_fail(client):
    response = client.get(reverse("user_details"))

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_user_endpoint__change_password__new_password_not_matching_with_400_response(
    authenticated_client, user_data
):
    password_info = {
        "old_password": user_data["password1"],
        "new_password1": "testpassword_new_new",
        "new_password2": "testpassword_new",
    }
    response = authenticated_client.post(reverse("rest_password_change"), password_info)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_user_endpoint__update_profile_have_no_effect(
    authenticated_client,
    normal_user,
    create_profile_for_normal_user,
):
    profile = normal_user.profile

    profile_data = {
        "gender": "F",
        "country": "Taiwan",
        "phone_number": "+8869000000000",
    }

    response = authenticated_client.put(reverse("user_details"), profile_data)

    assert response.status_code == status.HTTP_200_OK

    profile.refresh_from_db()
    assert profile.gender != profile_data["gender"]
    assert profile.country != profile_data["country"]
    assert profile.phone_number != profile_data["phone_number"]
