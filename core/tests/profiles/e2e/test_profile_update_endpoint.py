import pytest
from django.urls import reverse
from pytest_bdd import given, scenarios, then, when
from rest_framework import status

pytestmark = pytest.mark.django_db

scenarios("./features/profile__update.feature")

UPDATE_PROFILE_URL = reverse("me_update_profile")
"""
Feature: Profile update
    Given user update info
    When hitting me_update_profile with authed client
    Then I should get response 200 ok 
    * response data updated correct
"""


@given("user update info", target_fixture="update_info")
def _(mock_image_upload):
    return {
        "country": "US",
        "twitter_handle": "@test_123",
        "phone_number": "+1-418-543-8090",
        "about_me": "I'm American",
        "profile_photo": mock_image_upload,
    }


@when("hitting me_update_profile with authed client", target_fixture="response")
def _(update_info, authenticated_client, create_profile):
    return authenticated_client.patch(UPDATE_PROFILE_URL, data=update_info)


@then("I should get response 200 ok")
def _(response):
    assert response.status_code == status.HTTP_200_OK


@then("response data updated correct")
def _(response, normal_user):
    normal_user.refresh_from_db()
    profile = normal_user.profile
    assert response.data["country"] == profile.country
    assert response.data["twitter_handle"] == profile.twitter_handle
    assert response.data["phone_number"] == profile.phone_number
    assert response.data["about_me"] == profile.about_me
    assert response.data["profile_photo"] == profile.profile_photo.url
