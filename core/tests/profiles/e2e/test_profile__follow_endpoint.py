from uuid import uuid4

import pytest
from django.urls import reverse
from pytest_bdd import given, scenarios, then, when
from rest_framework import status

from core.apps.profiles.exceptions import (
    CantFollowYourselfException,
    FollowUnfollowTargetNotFound,
    RepeatFollowException,
    UnfollowButNotYetFollowException,
)

pytestmark = [
    pytest.mark.django_db,
    pytest.mark.e2e,
    pytest.mark.profile(type="follow_endpoint"),
]


scenarios("./features/profile__follow.feature")
"""
    Background:
        Given a fan user with profile exists
        And an idol user with profile exists
        And a client authenticated with fan
"""


@given("a fan user with profile exists", target_fixture="fan")
def _(profile_factory):
    return profile_factory.create()


@given("an idol user with profile exists", target_fixture="idol")
def _(profile_factory):
    return profile_factory.create()


@given("client authenticate with fan", target_fixture="client")
def _(fan, client):
    client.force_authenticate(user=fan.user)
    return client


@given("fan has followed idol", target_fixture="fan_has_idol")
def _(fan, idol):
    fan.following.add(idol)
    return fan


"""

    Scenario: Follow other user successful
        When fan follows idol, email should be sent
        Then fan should get 200 ok & success message
"""


@when("fan follows idol, email should be sent", target_fixture="response")
def _(idol, client, mocker):
    mock_inform_followed = mocker.patch("core.celery.task.inform_followed.delay")
    response = client.post(reverse("follow", args=[idol.id]))

    mock_inform_followed.assert_called_once()
    return response


@then("fan should get 200 ok & success message")
def _(response, idol, fan):
    assert response.status_code == status.HTTP_200_OK
    assert (
        response.data["message"] == f"You successfully followed {idol.user.full_name}."
    )
    assert fan.following.count() == 1
    assert fan.following.filter(id=idol.id).exists()


"""
    Scenario: Follow non-existing user should fail
        When fan follows none-existing user
        Then the fan should get 400 bad request & follow failed message

"""


@when("fan follows none-existing user", target_fixture="response")
def _(client):
    return client.post(reverse("follow", args=[uuid4()]))


@then("fan should get 404 not found & follow failed message")
def _(response, fan):
    assert response.status_code == FollowUnfollowTargetNotFound.status_code
    assert response.data["detail"] == FollowUnfollowTargetNotFound.default_detail
    assert fan.following.count() == 0


"""
    Scenario: Repeat follow should fail
        Given fan has followed idol
        When fan follows idol
        Then the fan should get 400 bad request & repeat follow failed message
"""


@when("fan follows idol", target_fixture="response")
def _(client, idol):
    return client.post(reverse("follow", args=[idol.id]))


@then(
    "the fan should get 400 bad request & repeat follow failed message",
    target_fixture="response",
)
def _(response, fan):
    assert response.status_code == RepeatFollowException.status_code
    assert response.data["detail"] == RepeatFollowException.default_detail
    assert fan.following.count() == 1


"""
    Scenario: Follow self should fail
        Given a user with profile exists
        When the user follows self
        Then fan should get 400 bad request & follow self failed message
"""


@when("the fan follows self", target_fixture="response")
def _(fan, client):
    return client.post(reverse("follow", args=[fan.id]))


@then("the fan should get 400 bad request & follow self failed message")
def _(response, fan):
    assert response.status_code == CantFollowYourselfException.status_code
    assert response.data["detail"] == CantFollowYourselfException.default_detail
    assert fan.following.count() == 0


"""

    Scenario: Unfollow a user success
        Given fan has followed idol
        When the fan unfollows idol
        Then fan should get 200 ok & unfollow success message
"""


@when("the fan unfollows idol", target_fixture="response")
def _(client, idol, fan_has_idol):
    assert fan_has_idol.following.count() == 1
    return client.post(reverse("unfollow", args=[idol.id]))


@then("fan should get 200 ok & unfollow success message")
def _(response, idol, fan_has_idol):
    assert response.status_code == status.HTTP_200_OK
    assert response.data["message"] == f"You have unfollowed {idol.user.full_name}."
    assert fan_has_idol.following.count() == 0


"""
Scenario: Unfollow non-existing user should fail
        When fan unfollows non-existing user
        Then the fan should get 400 bad request & failed message
"""


@when("fan unfollows none-existing user", target_fixture="response")
def _(client):
    return client.post(reverse("unfollow", args=[uuid4()]))


@then("fan should get 404 not found & unfollow failed message")
def _(response):
    assert response.status_code == FollowUnfollowTargetNotFound.status_code
    assert response.data["detail"] == FollowUnfollowTargetNotFound.default_detail


"""
    Scenario: Unfollow user you haven't followed should fail
        When fan tries to unfollow a user that they haven't followed
        Then fan should get 400 bad request & unfollow failed message
"""


@when(
    "fan tries to unfollow a user that they haven't followed", target_fixture="response"
)
def _(client, idol):
    return client.post(reverse("unfollow", args=[idol.id]))


@then("fan should get 400 bad request & unfollow failed message")
def _(response):
    assert response.status_code == UnfollowButNotYetFollowException.status_code
    assert response.data["detail"] == UnfollowButNotYetFollowException.default_detail
