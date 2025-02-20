import re

import pytest
from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from django.core import mail
from django.urls import reverse
from pytest_bdd import given, parsers, scenario, then, when
from rest_framework import status

pytestmark = [
    pytest.mark.django_db,
    pytest.mark.e2e,
    pytest.mark.user(type="registraion_endpoint"),
]


User = get_user_model()


@scenario("./features/auth.feature", "Regiter New User")
def test_registration():
    pass


@scenario("./features/auth.feature", "Reset Password")
def test_rest_password():
    pass


@given("I register user with correct data")
def register_user(
    user_data,
    mock_create_user_side_effect,
    client,
):
    # Register user
    response = client.post(reverse("rest_register"), user_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert len(mail.outbox) == 1


@when("after verified the email")
def veryfiy_email(client, user_data):
    # Get the validation key from mail body
    email_content = mail.outbox.pop(0)
    confirmation_lint = re.search(
        r"http://.*?/account-confirm-email/.*?/", email_content.body
    ).group(0)
    key = confirmation_lint.split("/")[-2]

    # Veryfy email
    response = client.post(reverse("rest_verify_email"), {"key": key})
    assert response.status_code == status.HTTP_200_OK

    user = EmailAddress.objects.get(email=user_data["email"])
    assert user.verified


@then("I should be able to login & get my access token")
def login_user(user_data, client):
    # Login user
    login_data = {"email": user_data["email"], "password": user_data["password1"]}
    response = client.post(reverse("rest_login"), login_data)

    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data


@given("Hitting reset password endpoint w/ email & receive confirm email")
def reset_password(normal_user, authenticated_client):
    # Request password reset
    response = authenticated_client.post(
        reverse("rest_password_reset"), {"email": normal_user.email}
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(mail.outbox) == 1


@when(parsers.parse("Hitting reset confirm enpoin w/ uid, token & ${new_password}"))
def confirm_reset_password(authenticated_client, new_password):
    # Get uid and token from confirmation link
    email_content = mail.outbox.pop(0)

    confirmation_link = re.search(
        "http://.*?/password_rest/confirm/.*?/.*?/", email_content.body
    ).group(0)

    split_link = confirmation_link.split("/")
    uid = split_link[-3]
    token = split_link[-2]

    # Confirm reset request
    confirm_data = {
        "new_password1": new_password,
        "new_password2": new_password,
        "uid": uid,
        "token": token,
    }
    response = authenticated_client.post(
        reverse("password_reset_confirm", args={"uid64": uid, "token": token}),
        confirm_data,
    )
    assert response.status_code == status.HTTP_200_OK


@then(parsers.parse("I should be able to login with ${new_password}"))
def login_with_new_password(client, normal_user, new_password):
    login_data = {"email": normal_user.email, "password": new_password}
    response = client.post(reverse("rest_login"), data=login_data)
    assert response.status_code == status.HTTP_200_OK
