import pytest
from pytest_factoryboy import register

from .documents import MockArticleDocument
from .factories import ArticleClapFactory, ArticleFactory, ArticleViewFactory

register(ArticleFactory)
register(ArticleViewFactory)
register(ArticleClapFactory)


@pytest.fixture
def article(article_factory):
    return article_factory.create()


@pytest.fixture
def setup_article_doc_index():
    MockArticleDocument._get_connection()
    MockArticleDocument._index.delete(ignore=[404])
    MockArticleDocument._index.create()

    yield

    MockArticleDocument._index.delete(ignore=[404])
