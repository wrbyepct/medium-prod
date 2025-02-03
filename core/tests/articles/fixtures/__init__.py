import pytest
from pytest_factoryboy import register

from .documents import TestArticleDocument
from .factories import ArticleClapFactory, ArticleFactory, ArticleViewFactory

register(ArticleFactory)
register(ArticleViewFactory)
register(ArticleClapFactory)


@pytest.fixture
def article(article_factory):
    return article_factory.create()


@pytest.fixture
def setup_article_doc_index():
    TestArticleDocument._get_connection()
    TestArticleDocument._index.delete(ignore=[404])
    TestArticleDocument._index.create()

    yield

    TestArticleDocument._index.delete(ignore=[404])


@pytest.fixture
def api_request_with_user(mocker):
    def _make_request(user="fake_user"):
        request = mocker.Mock()
        request.user = user
        return request

    return _make_request
