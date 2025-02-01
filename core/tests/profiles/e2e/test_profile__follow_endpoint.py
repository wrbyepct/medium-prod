from uuid import uuid4

import pytest
from django.urls import reverse
from pytest_bdd import given, scenarios, then, when
from rest_framework import status

pytestmark = pytest.mark.django_db

scenarios("./features/profile__follow.feature")
"""
    Background:
        Given a fan user with profile exists
        * an idol user with profile exists
        * client authenticate with fan
"""


@given("a fan user with profile exists", target_fixture="fan")
def _(profile_factory):
    p = profile_factory.create()
    return p.user


@given("an idol user with profile exists", target_fixture="idol")
def _(profile_factory):
    p = profile_factory.create()
    return p.user


@given("client authenticate with fan", target_fixture="client")
def _(fan, client):
    client.force_authenticate(user=fan)
    return client


"""

    Scenario: Follow other user successful
        When fan follows idol, email should be sent
        Then fan should get 200 ok & success message
"""


@when("fan follows idol, email should be sent", target_fixture="response")
def _(idol, client, mocker):
    mock_inform_followed = mocker.patch("core.apps.profiles.views.inform_followed")
    response = client.post(reverse("follow", args=[str(idol.id)]))

    mock_inform_followed.assert_called_once()
    return response


@then("fan should get 200 ok & success message")
def _(response, idol):
    assert response.status_code == status.HTTP_200_OK
    assert response.data["message"] == f"You successfully followed {idol.full_name}."


"""
    Scenario: Follow non-existing user should fail
        When fan follows none-existing user
        Then the fan should get 400 bad request & follow failed message

"""


@when("fan follows none-existing user", target_fixture="response")
def _(client):
    return client.post(reverse("follow", args=[uuid4()]))


@then("fan should get 404 not found & follow failed message")
def _(response):
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data["detail"] == "You can't follow a profile that does not exist."


"""
    Scenario: Repeat follow should fail
        Given fan has followed idol
        When fan follows idol
        Then the fan should get 400 bad request & repeat follow failed message
"""


@given("fan has followed idol")
def _(fan, idol):
    fan.profile.following.add(idol.profile)


@when("fan follows idol", target_fixture="response")
def _(client, idol):
    return client.post(reverse("follow", args=[idol.id]))


@then(
    "the fan should get 400 bad request & repeat follow failed message",
    target_fixture="response",
)
def _(response):
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["message"] == "You already followed that user."


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
def _(response):
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["message"] == "You can't follow yourself."


"""

    Scenario: Unfollow a user success
        Given fan has followed idol
        When the fan unfollows idol
        Then fan should get 200 ok & unfollow success message
"""


@when("the fan unfollows idol", target_fixture="response")
def _(client, idol):
    return client.post(reverse("unfollow", args=[idol.id]))


@then("fan should get 200 ok & unfollow success message")
def _(response, idol):
    assert response.status_code == status.HTTP_200_OK
    assert response.data["message"] == f"You have unfollowed {idol.full_name}."


"""
Scenario: Unfollow non-existing user should fail
        When fan unfollows none-existing user
        Then the fan should get 400 bad request & failed message
"""


@when("fan unfollows none-existing user", target_fixture="response")
def _(client):
    return client.post(reverse("unfollow", args=[uuid4()]))


@then("fan should get 404 not found & unfollow failed message")
def _(response):
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert (
        response.data["detail"] == "You can't unfollow a profile that does not exist."
    )


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
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert (
        response.data["message"]
        == "You can't unfollow a user that you haven't follwoed!"
    )
