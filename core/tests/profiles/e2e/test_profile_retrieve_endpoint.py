import pytest
from django.urls import reverse
from pytest_bdd import given, scenarios, then, when
from rest_framework import status

pytestmark = pytest.mark.django_db


"""
Feature: Profile retrieve
    Scenario: Hit 'me' endpoint unauthed should fail
        Given an unauthed client hitting 'all_profiles' endpoint
        Then I should get response 401 unauthorized
"""
scenarios("./features/profile__retrieve.feature")

ME_PROFILE_URL = reverse("me")


@given("an unauthed client hitting 'all_profiles' endpoint", target_fixture="response")
def _(client):
    return client.get(ME_PROFILE_URL)


@then("I should get response 401 unauthorized")
def _(response):
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


"""
    Scenario: Hit 'me' endpoint authed success
        Given a user with profile
        When hitting 'me' url with client authend by the user
        Then I should get response 200 ok
"""


@given("a user with profile", target_fixture="client")
def _(profile_factory, client):
    profile = profile_factory.create()
    user = profile.user
    client.force_authenticate(user=user)
    return client


@when("hitting 'me' url with client authend by the user", target_fixture="response")
def _(client):
    return client.get(ME_PROFILE_URL)


@then("I should get response 200 ok")
def _(response):
    assert response.status_code == status.HTTP_200_OK
