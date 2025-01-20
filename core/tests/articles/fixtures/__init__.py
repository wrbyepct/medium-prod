from unittest.mock import patch

import pytest
from faker import Faker
from pytest_factoryboy import register

from core.tests.utils.misc import create_upload_image_file


from .factories import ArticleClapFactory, ArticleFactory, ArticleViewFactory

register(ArticleFactory)
register(ArticleViewFactory)
register(ArticleClapFactory)

fake = Faker()


@pytest.fixture
def article(article_factory):
    return article_factory.create()


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
