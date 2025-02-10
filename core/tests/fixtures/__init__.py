from unittest.mock import patch

import pytest
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory
from faker import Faker

from core.apps.bookmarks.models import ReadingCategory
from core.tests.utils.misc import create_upload_image_file

from .constants import (
    ARTICLE_DOCUMENT_DELETE,
    ARTICLE_DOCUMENT_UPDATE,
    CREATE_USER_SIDE_EFFECT,
    PROFILE_CREATE,
    READING_CATEGORY_CREATE,
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
fake = Faker()


@pytest.fixture
def mock_request():
    request = RequestFactory().get("/")
    middleware = SessionMiddleware(lambda req: None)
    middleware.process_request(request=request)
    request.session.save()
    return request


@pytest.fixture
def api_request_with_user(mocker):
    def _make_request(user="fake_user"):
        request = mocker.Mock()
        request.user = user
        return request

    return _make_request


@pytest.fixture
def mock_article_index_update():
    with patch(ARTICLE_DOCUMENT_UPDATE):
        yield


@pytest.fixture
def mock_article_index_delete():
    with patch(ARTICLE_DOCUMENT_DELETE):
        yield


@pytest.fixture
def mock_create_user_side_effect():
    with patch(CREATE_USER_SIDE_EFFECT):
        yield


@pytest.fixture
def mock_profile_create():
    with patch(PROFILE_CREATE):
        yield


@pytest.fixture
def mock_reading_category_create():
    with patch(READING_CATEGORY_CREATE):
        yield


@pytest.fixture
def ipv4():
    return fake.ipv4()


@pytest.fixture
def mock_media_dir(tmpdir):
    with patch("django.conf.settings.MEDIA_ROOT", new=str(tmpdir)):
        yield


@pytest.fixture
def mock_image_upload():
    return create_upload_image_file()


@pytest.fixture
def create_profile(normal_user, profile_factory):
    profile_factory.create(user=normal_user)


@pytest.fixture
def create_reading_category(normal_user):
    # TODO change ReadingCategory to factory later
    ReadingCategory.objects.create(user=normal_user)
