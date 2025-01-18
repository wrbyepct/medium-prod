import re

import pytest
from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from django.core import mail
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


User = get_user_model()


def test_user_register_flow(mock_create_user_side_effect, user_data):
    client = APIClient()  # only it can store crendietial token

    # Register user
    response = client.post(reverse("rest_register"), user_data)
    assert response.status_code == status.HTTP_201_CREATED

    # Get the validation key from mail body

    email_content = mail.outbox.pop(0)
    confirmation_lint = re.search(
        r"http://.*?account-confirm-email/.*?/", email_content.body
    ).group(0)
    key = confirmation_lint.split("/")[-2]

    # Veryfy email
    response = client.post(reverse("rest_verify_email"), {"key": key})
    assert response.status_code == status.HTTP_200_OK

    user = EmailAddress.objects.get(email=user_data["email"])
    assert user.verified

    # Login user
    login_data = {"email": user_data["email"], "password": user_data["password1"]}
    response = client.post(reverse("rest_login"), login_data)
    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data


def test_user_flow_rest_password_flow_successful(normal_user):
    # Request password reset
    authenticated_client = APIClient(user=normal_user)
    response = authenticated_client.post(
        reverse("rest_password_reset"), {"email": normal_user.email}
    )
    assert response.status_code == status.HTTP_200_OK
    # Get uid and token from confirmation link
    email_content = mail.outbox.pop(0)

    confirmation_link = re.search(
        "http://.*?password_rest/confirm/.*?/.*?/", email_content.body
    ).group(0)

    split_link = confirmation_link.split("/")
    uid = split_link[-3]
    token = split_link[-2]

    # Confirm reset request
    confirm_data = {
        "new_password1": "testpassword_new_2",
        "new_password2": "testpassword_new_2",
        "uid": uid,
        "token": token,
    }
    response = authenticated_client.post(
        reverse("password_reset_confirm", args={"uid64": uid, "token": token}),
        confirm_data,
    )

    assert response.status_code == status.HTTP_200_OK

    user = User.objects.get(pk=normal_user.pk)
    assert user.check_password(confirm_data["new_password1"])
