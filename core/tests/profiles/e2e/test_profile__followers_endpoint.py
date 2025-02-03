import pytest
from django.urls import reverse
from pytest_bdd import given, scenarios, then, when
from rest_framework import status

from core.apps.profiles.serializers import FollowingSerializer

pytestmark = pytest.mark.django_db

scenarios("./features/profile__get_user_followers.feature")

""" 
    Scenario: Get User Followers
        Given a profile with followers exists
        When hitting profile user_follower enpdoint
        Then I should get 200 ok response from user_followers endpoint
        * the user's followers profiles data correct
"""


@given("a profile with followers exists", target_fixture="idol")
def _(profile_factory):
    return profile_factory.create(with_followers=3)


@when("hitting profile user_follower enpdoint", target_fixture="response")
def _(idol, authenticated_client):
    user_id = idol.user.id
    return authenticated_client.get(reverse("user_followers", args=[user_id]))


@then("I should get 200 ok response from user_followers endpoint")
def _(response):
    assert response.status_code == status.HTTP_200_OK


@then("the user's followers profiles data correct")
def _(response, idol):
    followers = idol.followers.all()
    serializer = FollowingSerializer(followers, many=True)

    assert response.data["followers_count"] == len(serializer.data)
    assert response.data["followers"] == serializer.data


"""
        Given a profile with following of 3 exists
        When hitting profile user_following endpoint
        Then I should get 200 ok response 
        And the user's following profiles
"""


@given("a profile with following of 3 exists", target_fixture="fan")
def profile_with_followings(profile_factory):
    return profile_factory.create(with_following=3)


@when("hitting profile user_following endpoint", target_fixture="response")
def hitting_profile_user_following_endpoint(fan, authenticated_client):
    user_id = fan.user.id
    return authenticated_client.get(reverse("user_following", args=[user_id]))


@then("I should get 200 ok response from user_following endpoint")
def assert_response_ok(response):
    assert response.status_code == status.HTTP_200_OK


@then("the user's following profile data correct")
def assert_response_data_correct(response, fan):
    profiles = fan.following.all()
    serializer = FollowingSerializer(profiles, many=True)

    assert response.data["following_count"] == len(serializer.data)
    assert response.data["following"] == serializer.data
