import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

pytestmark = [
    pytest.mark.django_db,
    pytest.mark.e2e,
    pytest.mark.user(type="detail_endpoint"),
]
User = get_user_model()


def test_user_view__retrieve_user_detail_successful(
    authenticated_client, normal_user, profile_factory
):
    # Arrange
    profile_factory.create(user=normal_user)

    resp = authenticated_client.get(reverse("user_details"))
    assert resp.status_code == status.HTTP_200_OK

    # Assert basic info
    assert "id" in resp.data
    assert resp.data["id"] == str(normal_user.id)

    assert "email" in resp.data
    assert resp.data["email"] == normal_user.email

    assert "first_name" in resp.data
    assert resp.data["first_name"] == normal_user.first_name

    assert "last_name" in resp.data
    assert resp.data["last_name"] == normal_user.last_name

    # Assert profile info
    profile = normal_user.profile
    assert "gender" in resp.data
    assert resp.data["gender"] == profile.gender

    assert "phone_number" in resp.data
    assert resp.data["phone_number"] == profile.phone_number

    assert "profile_photo" in resp.data
    assert resp.data["profile_photo"] == profile.profile_photo.url

    assert "country" in resp.data
    assert resp.data["country"] == profile.country

    assert "city" in resp.data
    assert resp.data["city"] == profile.city


def test_user_view__update_user_detail_successful(authenticated_client, normal_user):
    new_data = {
        "email": "test2@exmaple.com",
        "first_name": "New_first",
        "last_name": "New_last",
    }

    resp = authenticated_client.patch(reverse("user_details"), data=new_data)

    assert resp.status_code == status.HTTP_200_OK
    assert normal_user.email == new_data["email"]
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
