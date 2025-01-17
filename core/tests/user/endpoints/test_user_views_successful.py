import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

pytestmark = pytest.mark.django_db
User = get_user_model()


def test_user_view__retrieve_user_detail_successful(authenticated_client):
    response = authenticated_client.get(reverse("user_details"))
    assert response.status_code == status.HTTP_200_OK
    assert "id" in response.data
    assert "email" in response.data
    assert "first_name" in response.data
    assert "last_name" in response.data
    assert "gender" in response.data
    assert "phone_number" in response.data
    assert "profile_photo" in response.data
    assert "country" in response.data
    assert "city" in response.data


def test_user_view__update_user_detail_successful(authenticated_client, normal_user):
    new_data = {
        "first_name": "New_first",
        "last_name": "New_last",
    }
    response = authenticated_client.patch(reverse("user_details"), data=new_data)
    assert response.status_code == status.HTTP_200_OK
    assert normal_user.first_name == new_data["first_name"]
    assert normal_user.last_name == new_data["last_name"]


def test_user_view__change_password_successful(
    authenticated_client, user_data, normal_user
):
    password_info = {
        "old_password": user_data["password1"],
        "new_password1": "testpassword_new",
        "new_password2": "testpassword_new",
    }

    response = authenticated_client.post(reverse("rest_password_change"), password_info)
    assert response.status_code == status.HTTP_200_OK

    user = User.objects.get(pk=normal_user.pk)
    assert user.check_password(password_info["new_password1"])
