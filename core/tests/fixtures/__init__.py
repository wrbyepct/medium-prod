from unittest.mock import patch

import pytest
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory

from .constants import (
    ARTICLE_DOCUMENT_UPDATE,
    CREATE_USER_PROFILE_SIDE_EFFECT,
    CREATE_USER_READINGCATEGORY_SIDE_EFFECT,
)

"""
Q: Why Mock Request with SessionMiddleWare is Needed?

A: The functions from 'allauth' need it:

    def unstash_verified_email(self, request):
            ret = request.session.get("account_verified_email")
    >       request.session["account_verified_email"] = None
    E       TypeError: 'Mock' object does not support item assignment

    Those functions are used in CustomRegisterSerializer's .save()

Q: Then How do We mock it?
A: Mock it with django.test.RequestFactory
"""


@pytest.fixture
def mock_request():
    request = RequestFactory().get("/")
    middleware = SessionMiddleware(lambda req: None)
    middleware.process_request(request=request)
    request.session.save()
    return request


@pytest.fixture
def mock_article_index_update():
    with patch(ARTICLE_DOCUMENT_UPDATE):
        yield


@pytest.fixture
def mock_create_user_profile():
    with patch(CREATE_USER_PROFILE_SIDE_EFFECT):
        yield


@pytest.fixture
def mock_create_user_reading_category():
    with patch(CREATE_USER_READINGCATEGORY_SIDE_EFFECT):
        yield
